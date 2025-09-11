#!/usr/bin/env python

#
# Copyright (c) 2025 Dmitry Arkhipov (grisumbras@yandex.ru)
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#


import argparse
import contextlib
import datetime
import jinja2
import json
import os
import os.path
import shutil
import subprocess
import sys
import urllib.parse
import yaml


default_superproject_url = 'https://github.com/boostorg/boost/'
default_superproject_ref = 'develop'

future_boost_version = '1.90.0'
b2_version = '5.3.0'


def main(argv):
    args = parse_args(argv)

    runner = Runner()
    fs = FileSystem(args.cleanup)
    git = Git(runner, fs, args.allow_reuse)

    module_registry = dict()
    with git.clone_ref(args.url, args.ref, bare=True) as root:
        boost = SuperProject(root, args.url, args.ref, git)
        module_registry['boost'] = boost
        for submodule in boost.submodules(git):
            module_registry[submodule.name] = submodule

    template_env = jinja2.Environment(
        loader=jinja2.FunctionLoader(get_template),
        autoescape=False,
        undefined=jinja2.StrictUndefined,
        extensions=['jinja2.ext.do', 'jinja2.ext.loopcontrols'],
    )
    template_env.filters['slugify'] = slugify

    for module in module_registry.values():
        module.collect_data(git, fs, module_registry)

    for module in module_registry.values():
        module.generate_recipe(args.target, module_registry, template_env, fs)


def collect_dependencies(lib_dir, registry, fs):
    try:
        deps = collect_deps_from_build_jam(lib_dir, fs)
    except FileNotFoundError:
        deps = []
    if not deps:
        try:
            deps = collect_deps_from_cml(lib_dir, fs)
        except FileNotFoundError:
            print(f"failed to determine dependencies of '{lib_dir}'...")
    return [registry[dep] for dep in sorted(set(deps))]


def collect_deps_from_build_jam(lib_dir, fs):
    with fs.open(os.path.join(lib_dir, 'build.jam'), 'r') as f:
       lines = f.readlines()
       while lines:
           if lines[0].lstrip().startswith('constant boost_dependencies'):
               break
           lines = lines[1:]
       deps = ''
       while lines:
           deps += ' ' + lines[0].rstrip()
           if lines[0].rstrip().endswith(';'):
               break
           lines = lines[1:]
       if not deps:
           return []
       return [
           dep.split('/')[2]
           for dep in deps.split(': ')[1].split(' ;')[0].split(' ')
           if dep
       ]


def collect_deps_from_cml(lib_dir, fs):
    with fs.open(os.path.join(lib_dir, 'CMakeLists.txt'), 'r') as f:
       deps = []
       for line in f.readlines():
           if line.lstrip().startswith('Boost::'):
               dep = line.strip().split(':')[2]
               deps.append(fix_dep_name_for_cml(dep))
       return [dep for dep in deps if dep != 'headers']


def fix_dep_name_for_cml(name):
    if name == 'numeric_ublas':
        return 'ublas'
    if name == 'numeric_interval':
        return 'interval'
    if name.startswith('asio'):
        return 'asio'
    return name


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='Create Conan recipes for modular Boost builds.',
    )
    parser.add_argument(
        '--url',
        default=default_superproject_url,
        help=f'Boost superproject git url (default: {default_superproject_url}',
    )
    parser.add_argument(
        '--ref',
        default=default_superproject_ref,
        help=f'Boost superproject git ref to use (default: {default_superproject_ref})',
    )
    parser.add_argument(
        '-T', '--target',
        default='.',
        help='target directory (default: CWD)',
    )
    parser.add_argument(
        '--no-cleanup',
        action='store_false',
        default=True,
        dest='cleanup',
        help='do not remove temporary files',
    )
    parser.add_argument(
        '--allow-reuse',
        action='store_true',
        default=False,
        help='allow reuse of temporary files',
    )
    return parser.parse_args(argv[1:])


class Project():
    @property
    def conan_version(self):
        if self.git_ref in ('develop', 'master'):
            return (
                f'{future_boost_version}-{self.git_ref}'
                f'+{self.datetime.strftime("%y.%m.%d")}')
        elif self.git_ref.startswith('boost-'):
            return self.git_ref[6:]
        else:
            return self.git_ref

    @property
    def conan_ref(self):
        return f'{self.conan_name}/{self.conan_version}'

    def __init__(self, name, relative_path):
        self.name = name
        self.relative_path = relative_path

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Project("{self.name}", "{self.git_ref}")'


class SuperProject(Project):
    @property
    def conan_name(self):
        return slugify(self.name)

    def __init__(self, path, url, git_ref, git):
        super().__init__('boost', '.')
        self.git_ref = git_ref
        self.path = path
        self.url = url
        self.commit = git.get_commit(path)
        self.datetime = git.get_datetime(path)

    def submodules(self, git):
        submodules = git.submodule_config(
            self.path, '--name-only', '--get-regexp', 'path')
        for m in submodules:
            name = m.split('.')[1]
            raw_params = git.submodule_config(
                self.path, '--get-regexp', f'submodule\\.{name}\\.')
            path = None
            url = None
            for p in raw_params:
                k, v = p.split(' ')
                k = k.split('.')[2]
                if k == 'path':
                    path = v
                elif k == 'url':
                    url = v

                cls = IgnoredProject
                if path == 'libs/headers':
                    cls = IgnoredProject
                elif path.startswith('libs/'):
                    cls = LibraryProject

                yield cls(name, path, url, self, git)

    def collect_data(self, git, fs, module_registry):
        pass

    def generate_recipe(self, base_dir, registry, template_env, fs):
        print(f'skipping superproject')

    def __repr__(self):
        return f'SuperProject("{self.name}", "{self.git_ref}")'


class LibraryProject(Project):
    @property
    def conan_name(self):
        return f'boost-{slugify(self.name)}'

    @property
    def git_ref(self):
        return self.superproject.git_ref

    def __init__(self, name, path, url, superproject, git):
        super().__init__(name, path)
        self.superproject = superproject
        self.url = urllib.parse.urljoin(superproject.url, url)
        self.commit = git.submodule_commit(superproject.path, path)

    def collect_data(self, git, fs, registry):
        with git.clone_commit(self.url, self.commit, target=self.name) as lib:
            self.datetime = git.get_datetime(lib)

            meta_path = os.path.join(lib, 'meta', 'libraries.json')
            with fs.open(meta_path, 'r') as meta:
                metadata = json.load(meta)
                if type(metadata) == list:
                    metadata = metadata[0]
                for k, v in metadata.items():
                    if k == 'name':
                        continue
                    setattr(self, k, v)

            includedir = os.path.join(lib, 'include')
            for root, dirs, files in fs.walk(includedir):
                if files:
                    offset = len(includedir) + 1
                    self.header = os.path.join(root, files[0])[offset:]
                    break

            self.headeronly = not fs.exists(os.path.join(lib, 'build'))
            self.dependencies = collect_dependencies(lib, registry, fs)

    def generate_recipe(self, base_dir, registry, template_env, fs):
        pkg_base_dir = os.path.join(base_dir, 'recipes', self.conan_name)
        pkg_dir = os.path.join(pkg_base_dir, 'all')
        pkg_test_dir = os.path.join(pkg_dir, 'test_package')

        fs.create_path(pkg_test_dir)

        versions = dict()
        versions['versions'] = dict()
        versions['versions'][self.conan_version] = {'folder': 'all'}

        with fs.open(os.path.join(pkg_base_dir, 'config.yml'), 'w') as f:
            yaml.dump(versions, f)

        conandata = dict()
        conandata['sources'] = dict()
        conandata['sources'][self.conan_version] = {
            'url': self.url,
            'commit': self.commit,
            'dependencies': [dep.conan_ref for dep in self.dependencies],
        }

        with fs.open(os.path.join(pkg_dir, 'conandata.yml'), 'w') as f:
            yaml.dump(conandata, f)

        template = template_env.get_template('conanfile')
        with fs.open(os.path.join(pkg_dir, 'conanfile.py'), 'w') as f:
            template.stream({
                'project': self,
                'b2_version': b2_version,
            }).dump(f)

        template = template_env.get_template('test_conanfile')
        with fs.open(os.path.join(pkg_test_dir, 'conanfile.py'), 'w') as f:
            template.stream({ 'project': self }).dump(f)

        template = template_env.get_template('test_cml')
        with fs.open(os.path.join(pkg_test_dir, 'CMakeLists.txt'), 'w') as f:
            template.stream({ 'project': self }).dump(f)

        template = template_env.get_template('test_cpp')
        with fs.open(os.path.join(pkg_test_dir, 'test.cpp'), 'w') as f:
            template.stream({ 'project': self }).dump(f)

    def __repr__(self):
        return f'LibraryProject("{self.name}", "{self.git_ref}")'


class IgnoredProject(Project):
    def __init__(self, name, path, *args):
        super().__init__(name, path)

    def update_params(self, *args):
        pass

    def collect_data(self, *args):
        pass

    def generate_recipe(self, base_dir, registry, template_env, fs):
        print(f"skipping submodule '{self.relative_path}'")

    def __repr__(self):
        return f'IgnoredProject("{self.name}", "{self.git_ref}")'


class Git():
    def __init__(self, runner, fs, allow_reuse=False):
        self.runner = runner
        self.fs = fs
        self.allow_reuse = allow_reuse

    def clone_ref(self, repo, ref, target=None, bare=False):
        target = target or repo.split('/')[-1] or repo.split('/')[-2]

        args = ['git', 'clone', '--branch', ref, '--depth', '1']
        if bare:
            args.append('--bare')
        args += [repo, target]

        if not self.allow_reuse or not self.fs.exists(target):
            self.runner.run(*args)
        return self.fs.claim_directory(target)

    def clone_commit(self, repo, commit, target=None):
        target = target or repo.split('/')[-1] or repo.split('/')[-2]

        if not self.allow_reuse or not self.fs.exists(target):
            self.fs.create_path(target)
            self.runner.run('git', '-C', target, 'init', '-b', 'master')
            self.runner.run(
                'git', '-C', target, 'remote', 'add', 'origin', repo,
            )
            self.runner.run(
                'git', '-C', target, 'fetch', 'origin', commit, '--depth', '1',
            )
            self.runner.run(
                'git', '-C', target, 'reset', '--hard', 'FETCH_HEAD',
            )
        return self.fs.claim_directory(target)

    def get_commit(self, tree):
        return self._get_string(
            'git', '-C', tree, 'rev-list', 'HEAD', '-n', '1',
        )

    def get_datetime(self, tree):
        s = self._get_string(
            'git', '-C', tree, 'log', '-1', '--format=%ad',
            '--date=format:%Y-%m-%dT%H:%M',
        )
        return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M')

    def submodule_config(self, tree, *vargs):
        return self._get_lines(
            'git', '-C', tree, 'config', '--blob', 'HEAD:.gitmodules', *vargs,
        )

    def submodule_commit(self, tree, path):
        return self._get_string(
            'git', '-C', tree, 'ls-tree', 'HEAD', path, '--object-only',
        )

    def _get_string(self, *args):
        proc = self.runner.run(*args, stdout=subprocess.PIPE, text=True)
        return proc.stdout.strip()

    def _get_lines(self, *args):
        proc = self.runner.run(*args, stdout=subprocess.PIPE, text=True)
        return [line for line in proc.stdout.split('\n') if line]


class Runner():
    @staticmethod
    def run(*args, **kw):
        proc = subprocess.run(args, **kw)
        proc.check_returncode()
        return proc


class FileSystem():
    def __init__(self, cleanup=True):
        self.cleanup = cleanup

    @staticmethod
    def open(path, mode='r'):
        return open(path, mode, encoding='utf-8', errors='replace')

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def walk(path):
        return os.walk(path)

    @staticmethod
    def create_path(path):
        return os.makedirs(path, exist_ok=True)

    @contextlib.contextmanager
    def claim_directory(self, path):
        try:
            yield path
        finally:
            if self.cleanup:
                shutil.rmtree(path)


def slugify(text):
    result = ''
    for c in text:
        if not c.isalnum():
            if result and result[-1] != '-':
                result += '-'
        elif c.isupper():
            if result and result[-1] != '-':
                result + '-'
            result += c.lower()
        else:
            result += c
    return result


def get_template(name):
    if name == 'conanfile':
        return conanfile_template
    if name == 'test_conanfile':
        return test_conanfile_template
    if name == 'test_cml':
        return test_cml_template
    if name == 'test_cpp':
        return test_cpp_template

conanfile_template = '''\
import os.path
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy
from conan.tools.scm import Git

class Boost{{ project.name.title() }}Recipe(ConanFile):
    name = 'boost-{{project.name|slugify}}'

    license = 'BSL-1.0'
    description = '{{project.description}}'
    {% set sep = joiner(', ') -%}
    author = '{% for a in project.authors %}{{sep()}}{{a}}{% endfor %}'
    url = '{{project.url}}'
    topics = {{project.category}}

    {% if not project.headeronly -%}
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    {%- elif project.cxxstd is defined -%}
    settings = 'compiler'
    {%- endif %}

    package_type = {% if project.headeronly -%}
        'header-library'
    {%- else -%}
        'library'
    {%- endif %}

    {% if project.cxxstd is defined -%}
    def validate(self):
        check_min_cppstd(self, '{{project.cxxstd}}')
    {%- endif %}

    {% if not project.headeronly -%}
    def build_requirements(self):
       self.tool_requires('b2/[>={{ b2_version }}]')
    {%- endif %}

    def requirements(self):
        for dep in self.conan_data['sources'][self.version]['dependencies']:
            self.requires(
                dep,
                headers=True,
                transitive_headers=True,
            {%- if not project.headeronly %}
                libs=True,
                transitive_libs=True,
            {% endif -%}
            )

    def source(self):
        git = Git(self)
        data = self.conan_data['sources'][self.version]
        git.fetch_commit(data['url'], data['commit'])

    {% if project.headeronly -%}
    def build(self):
        pass

    def package(self):
        copy(self, '*',
            os.path.join(self.source_folder, 'include'),
            os.path.join(self.package_folder, 'include'))

    def package_id(self):
        self.info.clear()
    {%- endif %}

    def package_info(self):
        {% if project.headeronly -%}
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
        {%- endif %}
        self.cpp_info.set_property('cmake_target_name', 'Boost::{{project.name.title()}}')
        self.cpp_info.set_property('b2_project_name', '/boost/{{project.name|slugify}}')

'''

test_conanfile_template = '''\
import os

from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.build import can_run


class Boost{{ project.name.title() }}TestConan(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'CMakeDeps', 'CMakeToolchain'

    def requirements(self):
        self.requires(self.tested_reference_str)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def layout(self):
        cmake_layout(self)

    def test(self):
        if not can_run(self):
            return
        cmd = os.path.join(self.cpp.build.bindir, 'test')
        self.run(cmd, env="conanrun")
'''

test_cml_template = '''\
cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

find_package(boost-{{ project.name | slugify }} CONFIG REQUIRED)

add_executable(test test.cpp)
target_link_libraries(test Boost::{{ project.name.title() }})
'''

test_cpp_template = '''\
#include <{{ project.header }}>

int main()
{
    return 0;
}
'''

if __name__ == '__main__':
    main(sys.argv)
