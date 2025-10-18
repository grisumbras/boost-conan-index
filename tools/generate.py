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
import importlib.util
import jinja2
import json
import os
import os.path
import re
import shutil
import subprocess
import sys
import urllib.parse
import yaml


default_superproject_url = 'https://github.com/boostorg/boost/'
default_superproject_ref = 'develop'
index_url = 'https://github.com/grisumbras/boost/'

future_boost_version = '1.90.0'
b2_tools_version = '0.0.1-a'
b2_version = '5.3.0'


def main(argv):
    args = parse_args(argv)

    runner = Runner()
    fs = FileSystem(args.cleanup)
    git = Git(runner, fs, args.allow_reuse)

    tools = RecipeToolsProject()
    module_registry = {tools.name: tools}

    with git.clone_ref(args.url, args.ref, bare=True) as root:
        boost = SuperProject(root, args.url, args.ref, args.tool_ref, git)
        module_registry['boost'] = boost
        for submodule in boost.submodules(tools, git):
            module_registry[submodule.name] = submodule

    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates'),
            'utf-8',
        ),
        autoescape=False,
        undefined=jinja2.StrictUndefined,
        extensions=['jinja2.ext.do', 'jinja2.ext.loopcontrols'],
    )

    with module_registry['boostdep'].materialize(git) as depinst_dir:
        depinst = Depinst(depinst_dir)

    for module in module_registry.values():
        module.collect_data(git, fs, module_registry, depinst)

    for module in module_registry.values():
        module.generate_recipe(args.target, template_env, fs)


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
        '--tool-ref',
        default=default_superproject_ref,
        help=f'Tool subproject git ref to use (default: {default_superproject_ref})',
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


def collect_module_deps_from_jam_file(path, fs):
    with fs.open(path, 'r') as f:
        for line in f.readlines():
            stripped = line.lstrip()
            if stripped.startswith('import-search'):
                module = stripped.split(' ')[1]
                module = module.split('/')
                if module[:2] == ['', 'boost']:
                    yield module[2]


class Project():
    @property
    def conan_version(self):
        result = getattr(self, '_conan_version', None)
        if result is None:
            if self.git_ref in ('develop', 'master'):
                result = (
                    f'{future_boost_version}-a.{self.git_ref[0]}'
                    f'+{self.datetime.strftime("%y.%m.%d.%H.%M")}')
            elif self.git_ref.startswith('boost-'):
                result = self.git_ref[6:]
                parts = result.split('.')
                if len(parts) > 3:
                    pre = '.'.join(parts[3:])
                    if pre.startswith('beta'):
                        result = '.'.join(parts[:3]) + '-b.' + pre[4:]
                    else:
                        raise RuntimeError(
                            'unknown version pattern ' + self.git_ref,
                        )
            else:
                result = self.git_ref
            setattr(self, '_conan_version', result)
        return result

    @property
    def conan_ref(self):
        return f'{self.conan_name}/{self.conan_version}'

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Project("{self.name}")'


class SuperProject(Project):
    @property
    def conan_name(self):
        return self.name

    def __init__(self, path, url, git_ref, tool_git_ref, git):
        super().__init__('boost')
        self.git_ref = git_ref
        self.tool_git_ref = tool_git_ref
        self.path = path
        self.url = url
        self.commit = git.get_commit(path)
        self.datetime = git.get_datetime(path)

    def submodules(self, tools, git):
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

            if path == 'libs/headers':
                cls = IgnoredProject
            elif path.startswith('libs/'):
                cls = LibraryProject
            elif path.startswith('tools/'):
                cls = ToolProject
            else:
                cls = IgnoredProject

            yield cls(name, path, url, self, tools, git)

    def collect_data(self, *_):
        pass

    def generate_recipe(self, *_):
        print(f'skipping superproject')

    def __repr__(self):
        return f'SuperProject("{self.name}", "{self.git_ref}")'


class LibraryProject(Project):
    @property
    def conan_name(self):
        return f'boost-{self.name}'

    @property
    def git_ref(self):
        return self.superproject.git_ref

    def __init__(self, name, path, url, superproject, tools, git):
        super().__init__(name)
        self.superproject = superproject
        self.recipe_tools = tools
        self.url = urllib.parse.urljoin(superproject.url, url)
        self.commit = git.submodule_commit(superproject.path, path)
        self.dependencies = []
        self.cxxstd = None
        self.exceptions = None

    def collect_data(self, git, fs, registry, depinst):
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
            offset = len(includedir) + 1
            for root, _, files in fs.walk(includedir):
                if root[offset:].find('detail') >= 0:
                    continue
                if files:
                    self.header = os.path.join(root, files[0])[offset:]
                    break

            self.is_header_only = not fs.exists(os.path.join(lib, 'build'))
            self.dependencies = depinst(
                self, lib, registry,
            )

            exceptions = os.path.join(
                os.path.dirname(__file__), 'exceptions', self.name + '.py',
            )
            if fs.exists(exceptions):
                mod_name = 'boost.' + self.name + '.exceptions'
                spec = importlib.util.spec_from_file_location(
                    mod_name, exceptions,
                )
                mod = importlib.util.module_from_spec(spec)
                # sys.modules[mod_name] = mod
                spec.loader.exec_module(mod)
                mod.update_data(self, lib, registry)

    def generate_recipe(self, base_dir, template_env, fs):
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
            'kind': 'header-library' if self.is_header_only else 'library',
            'cxxstd': self.cxxstd,
            'dependencies': [
                {
                    'ref': dep.conan_ref,
                    'public': is_public,
                    'header': dep.is_header_only
                }
                for dep, is_public in self.dependencies
            ],
        }

        with fs.open(os.path.join(pkg_dir, 'conandata.yml'), 'w') as f:
            yaml.dump(conandata, f)

        template = template_env.get_template('conanfile.py.jinja')
        with fs.open(os.path.join(pkg_dir, 'conanfile.py'), 'w') as f:
            template.stream({
                'project': self,
                'b2_version': b2_version,
            }).dump(f)

        template = template_env.get_template('test_conanfile.py.jinja')
        with fs.open(os.path.join(pkg_test_dir, 'conanfile.py'), 'w') as f:
            template.stream({ 'project': self }).dump(f)

        template = template_env.get_template('test_cmakelists.txt.jinja')
        with fs.open(os.path.join(pkg_test_dir, 'CMakeLists.txt'), 'w') as f:
            template.stream({ 'project': self }).dump(f)

        template = template_env.get_template('test.cpp.jinja')
        with fs.open(os.path.join(pkg_test_dir, 'test.cpp'), 'w') as f:
            template.stream({ 'project': self }).dump(f)

        if self.exceptions:
            fs.copy(self.exceptions, os.path.join(pkg_dir, 'exceptions.py'))

    def __repr__(self):
        return f'LibraryProject("{self.name}", "{self.git_ref}")'


class ToolProject(Project):
    def __init__(self, name, path, url, superproject, tools, git):
        super().__init__(name)
        self.superproject = superproject
        self.url = urllib.parse.urljoin(superproject.url, url)
        self.ref = superproject.tool_git_ref

    def collect_data(self, *_):
        pass

    def generate_recipe(self, *_):
        print(f"skipping tool submodule '{self.name}'")

    @contextlib.contextmanager
    def materialize(self, git):
        with git.clone_ref(self.url, self.ref, target=self.name) as lib:
            try:
                yield lib
            finally:
                pass

    def __repr__(self):
        return f'ToolProject("{self.name}")'


class RecipeToolsProject(Project):
    @property
    def conan_version(self):
        return self.version

    @property
    def conan_name(self):
        return self.name

    def __init__(self):
        super().__init__('b2-tools')
        self.url = 'https://grisumbras/boost-conan-index'
        self.version = b2_tools_version
        self.b2_version = b2_version

    def collect_data(self, *_):
        pass

    def generate_recipe(self, base_dir, template_env, fs):
        pkg_base_dir = os.path.join(base_dir, 'recipes', 'b2-tools')
        pkg_dir = os.path.join(pkg_base_dir, 'all')
        pkg_test_dir = os.path.join(pkg_dir, 'test_package')

        fs.create_path(pkg_test_dir)

        versions = dict()
        versions['versions'] = dict()
        versions['versions'][self.version] = {'folder': 'all'}

        with fs.open(os.path.join(pkg_base_dir, 'config.yml'), 'w') as f:
            yaml.dump(versions, f)

        template = template_env.get_template('tools.py.jinja')
        with fs.open(os.path.join(pkg_dir, 'conanfile.py'), 'w') as f:
            template.stream({ 'project': self }).dump(f)

        fs.copy(
            os.path.join(os.path.dirname(__file__), '..', 'LICENSE_1_0.txt'),
            pkg_dir,
        )

        template = template_env.get_template('tools_test_conanfile.py.jinja')
        with fs.open(os.path.join(pkg_test_dir, 'conanfile.py'), 'w') as f:
            template.stream({ 'project': self }).dump(f)

        template = template_env.get_template('test_jamroot.jam.jinja')
        with fs.open(os.path.join(pkg_test_dir, 'jamroot.jam'), 'w') as f:
            template.stream({ 'project': self }).dump(f)

        template = template_env.get_template('tools_test.cpp.jinja')
        with fs.open(os.path.join(pkg_test_dir, 'test.cpp'), 'w') as f:
            template.stream({}).dump(f)

    def __repr__(self):
        return f'RecipeToolsProject()'


class IgnoredProject(Project):
    def __init__(self, name, *_):
        super().__init__(name)

    def collect_data(self, *_):
        pass

    def generate_recipe(self, *_):
        print(f"skipping submodule '{self.name}'")

    def __repr__(self):
        return f'IgnoredProject("{self.name}")'


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

    @staticmethod
    def copy(src, dst):
        shutil.copy(src, dst)


class Depinst():
    def __init__(self, location):
        mod_name = 'boostdep.depinst'
        depinst_dir = os.path.join(location, 'depinst')

        spec = importlib.util.spec_from_file_location(
            mod_name, os.path.join(depinst_dir, 'depinst.py'),
        )
        mod = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = mod
        spec.loader.exec_module(mod)
        self._module = mod

        # mod.verbose = -1
        mod.is_module = self._is_module

        exceptions = {}
        with open(os.path.join(depinst_dir, 'exceptions.txt'), 'r') as f:
            lib = None
            for line in f:
                line = line.rstrip()
                match = re.match('(.*):$', line)
                if match:
                    lib = match.group(1).replace('~', '/')
                else:
                    file = line.lstrip()
                    exceptions[file] = lib
        self._exceptions = exceptions

    def __call__(self, lib, lib_dir, registry):
        public_deps = {lib.name: 1}
        self._module.scan_directory(
            os.path.join(lib_dir, 'include'),
            self._exceptions,
            registry,
            public_deps,
            [],
        )

        private_deps = {lib.name : 1}
        for subdir in ['include', 'src', 'build']:
            self._module.scan_directory(
                os.path.join(lib_dir, subdir),
                self._exceptions,
                registry,
                private_deps,
                [],
            )

        private_deps = sorted(set(self._fix(dep) for dep in private_deps))
        public_deps = sorted(set(self._fix(dep) for dep in public_deps))
        return [
            (registry[dep], True) for dep in public_deps
            if dep != lib.name
        ] + [
            (registry[dep], False) for dep in private_deps
            if dep not in public_deps
        ]

    @staticmethod
    def _fix(dep):
        if dep == 'numeric/conversion':
            return 'numeric_conversion'
        if dep == 'numeric/odeint':
            return 'odeint'
        if dep == 'numeric/ublas':
            return 'ublas'
        if dep == 'numeric/interval':
            return 'interval'
        return dep

    @staticmethod
    def _is_module(name, registry):
        return Depinst._fix(name) in registry


if __name__ == '__main__':
    main(sys.argv)
