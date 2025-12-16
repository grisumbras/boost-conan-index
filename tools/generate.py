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
index_url = 'https://github.com/grisumbras/boost-conan-index/'

future_boost_version = '1.90.0'
b2_tools_version = '0.0.1-a'
b2_version = '5.3.0'


def main(argv):
    args = parse_args(argv)

    runner = Runner()
    fs = FileSystem(args.cleanup)
    git = Git(runner, fs, args.allow_reuse)

    tools = RecipeToolsProject()
    helpers = HelpersProject()
    module_registry = {tools.name: tools, helpers.name: helpers}

    with git.clone_ref(args.url, args.ref, bare=True) as root:
        boost = SuperProject(root, args.url, args.ref, args.tool_ref, git)
        module_registry['boost'] = boost
        for submodule in boost.submodules(tools, helpers, git):
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


def collect_libraries(lib_dir, lib_name, fs):
    lib_name = 'boost_' + lib_name
    return collect_libraries_from_jamfile(lib_dir, lib_name, fs) or [{
        'name': lib_name,
        'dependencies': [],
        'kind': (
            'library'
            if fs.exists(os.path.join(lib_dir, 'build'))
            else 'header-library'
        ),
    }]


def collect_libraries_from_jamfile(lib_dir, lib_name, fs):
    build_jam = os.path.join(lib_dir, 'build.jam')
    if not fs.exists(build_jam):
        return []

    with fs.open(build_jam, 'r') as f:
        lines = f.readlines()
        while lines:
            match = re.match(r'\s*call-if\s+: boost-library\b', lines[0])
            if match:
                break
            lines = lines[1:]

        targets = ''
        while lines:
            targets = targets + lines[0] + ' '
            if lines[0].find(';') >= 0:
                break
            lines = lines[1:]
        targets = targets.split(';', 1)[0].split(':')
        if len(targets) < 3:
            return []

        targets = [tgt.strip() for tgt in targets[2].strip().split(' ') if tgt]
        if len(targets) < 2 or targets[0] != 'install':
            return []

        targets = [tgt for tgt in targets[1:]]

        main_target = {
            'name': lib_name,
            'kind': 'library' if lib_name in targets else 'header-library',
            'dependencies': [],
        }

        return [main_target] + [
            {
                'name': target,
                'kind': 'library',
                'dependencies': [lib_name],
            }
            for target in targets
            if target != lib_name
        ]


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

    def submodules(self, tools, helpers, git):
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

            yield cls(name, path, url, self, tools, helpers, git)

    def collect_data(self, *_):
        pass

    def generate_recipe(self, *_):
        print(f'skipping superproject')

    def __repr__(self):
        return f'SuperProject("{self.name}", "{self.git_ref}")'


class LibraryProject(Project):
    @property
    def is_header_only(self):
        for tgt in self.targets:
            if tgt['kind'] == 'library':
                return False
        return True

    @property
    def conan_name(self):
        return f'boost-{self.name}'

    @property
    def git_ref(self):
        return self.superproject.git_ref

    def __init__(self, name, path, url, superproject, tools, helpers, git):
        super().__init__(name)
        self.superproject = superproject
        self.recipe_tools = tools
        self.boost_helpers = helpers
        self.url = urllib.parse.urljoin(superproject.url, url)
        self.commit = git.submodule_commit(superproject.path, path)
        self.dependencies = []
        self.targets = []
        self.cxxstd = None

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

            self.header = self._locate_header(lib, fs)
            self.targets = collect_libraries(lib, self.name, fs)
            self.dependencies = depinst(self, lib, registry)

            exceptions_func = getattr(self, f'_{self.name}_exceptions', None)
            if exceptions_func is not None:
                exceptions_func(lib, registry)

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
            'cxxstd': self.cxxstd,
            'targets': self.targets,
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

    def __repr__(self):
        return f'LibraryProject("{self.name}", "{self.git_ref}")'

    def _locate_header(self, lib_dir, fs):
        includedir = os.path.join(lib_dir, 'include')
        offset = len(includedir) + 1

        for convenience_header in (
            os.path.join(includedir, 'boost', self.name, self.name + '.hpp'),
            os.path.join(includedir, 'boost', self.name + '.hpp'),
        ):
            if fs.exists(convenience_header):
                return convenience_header[offset:]

        for root, _, files in fs.walk(includedir):
            if root[offset:].find('detail') >= 0:
                continue
            if files:
                return os.path.join(root, files[0])[offset:]

    def _context_exceptions(self, lib_dir, registry):
        self.header = 'boost/context/fiber.hpp'

    def _function_types_exceptions(self, lib_dir, registry):
        self.targets[0]['kind'] = 'header-library'

    def _graph_exceptions(self, lib_dir, registry):
        for i, dep in enumerate(self.dependencies):
            if dep[0].name == 'geometry':
                del self.dependencies[i]

    def _iostreams_exceptions(self, lib_dir, registry):
        for i, target in enumerate(self.targets):
            if target['name'] == '$(compression-libs-to-install)':
                del self.targets[i]

    def _math_exceptions(self, lib_dir, registry):
        for target in self.targets:
            if target['name'] == 'boost_math':
                target['kind'] = 'header-library'

    def _mpi_exceptions(self, lib_dir, registry):
        self.targets = [tgt for tgt in self.targets if tgt['name'] != 'mpi']

    def _test_exceptions(self, lib_dir, registry):
        self.header = 'boost/test/framework.hpp'
        has_predef = False
        for dep, _ in self.dependencies:
            has_predef = dep.name == 'predef'
        if not has_predef:
            self.dependencies.append( (registry['predef'], False) )
        self.targets = [
            {
                'name': 'boost_unit_test_framework',
                'kind': 'library',
                'dependencies': [],
            },
            {
                'name': 'boost_prg_exec_monitor',
                'kind': 'library',
                'dependencies': [],
            },
            {
                'name': 'boost_test_exec_monitor',
                'kind': 'library',
                'dependencies': [],
            },
        ]

    def _redis_exceptions(self, lib_dir, registry):
        self.dependencies.append( (ExternalProject('openssl'), True) )
        self.targets[0]['dependencies'].append('openssl::ssl')

    def _mysql_exceptions(self, lib_dir, registry):
        self.dependencies.append( (ExternalProject('openssl'), True) )
        self.targets[0]['dependencies'].append('openssl::ssl')

    def _system_exceptions(self, lib_dir, registry):
        self.targets[0]['kind'] = 'header-library'


class ToolProject(Project):
    def __init__(self, name, path, url, superproject, tools, helpers, git):
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
        self.url = index_url
        self.version = b2_tools_version

    def collect_data(self, *_):
        pass

    def generate_recipe(self, base_dir, template_env, fs):
        recipe_dir = os.path.join(base_dir, 'recipes', self.name)
        fs.copy_tree(
            os.path.join(os.path.dirname(__file__), self.name),
            recipe_dir,
            dirs_exist_ok=True,
        )

        versions = dict()
        versions['versions'] = dict()
        versions['versions'][self.version] = {'folder': 'all'}
        with fs.open(os.path.join(recipe_dir, 'config.yml'), 'w') as f:
            yaml.dump(versions, f)

        fs.copy(
            os.path.join(os.path.dirname(__file__), '..', 'LICENSE_1_0.txt'),
            recipe_dir,
        )

    def __repr__(self):
        return f'RecipeToolsProject()'


class HelpersProject(Project):
    @property
    def conan_version(self):
        return self.version

    @property
    def conan_name(self):
        return self.name

    def __init__(self):
        super().__init__('boost-helpers')
        self.url = index_url
        self.version = b2_tools_version

    def collect_data(self, *_):
        pass

    def generate_recipe(self, base_dir, template_env, fs):
        recipe_dir = os.path.join(base_dir, 'recipes', self.name)
        fs.copy_tree(
            os.path.join(os.path.dirname(__file__), self.name),
            recipe_dir,
            dirs_exist_ok=True,
        )

        versions = dict()
        versions['versions'] = dict()
        versions['versions'][self.conan_version] = {'folder': 'all'}
        with fs.open(os.path.join(recipe_dir, 'config.yml'), 'w') as f:
            yaml.dump(versions, f)

        data = {'b2_version': b2_version}
        with fs.open(os.path.join(recipe_dir, 'all', 'data.yml'), 'w') as f:
            yaml.dump(data, f)

        fs.copy(
            os.path.join(os.path.dirname(__file__), '..', 'LICENSE_1_0.txt'),
            recipe_dir,
        )

    def __repr__(self):
        return f'HelpersProject()'


class ExternalProject(Project):
    def __init__(self, name, version=None, header_only=False):
        super().__init__(name)
        self._conan_version = version if version is not None else '[*]'
        self.is_header_only = header_only

    @property
    def conan_name(self):
        return self.name


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

    @staticmethod
    def copy_tree(src, dst, dirs_exist_ok=False):
        shutil.copytree(src, dst, dirs_exist_ok=dirs_exist_ok)


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
