#
# Copyright (c) 2025 Dmitry Arkhipov (grisumbras@yandex.ru)
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#


import collections.abc
import glob
import os
import os.path
import shutil
from conan import ConanFile
from conan.tools.apple.apple import (
    is_apple_os,
    XCRun,
)
from conan.tools.env import Environment
from conan.tools.files import (
    chdir,
    save,
)
from conan.tools.microsoft.visual import msvc_version_to_vs_ide_version
from hashlib import md5
from jinja2 import Template


class B2RecipeToolsRecipe(ConanFile):
    name = 'b2-tools'
    description = 'Recipe tools for building with B2'
    author = 'Dmitry Arkhipov'
    url = 'https://grisumbras/boost-conan-index'
    license = 'BSL-1.0'
    package_type = 'python-require'
    exports = 'LICENSE_1_0.txt'


class B2Toolchain(object):
    def __init__(self, conanfile, generators_folder=None):
        self._conanfile = conanfile
        self.generators_folder = (
            generators_folder or conanfile.generators_folder
        )

        var = _collect_variations(conanfile)
        self.variation = {'toolset': var.get('toolset')}

        self._toolsets = {}
        self._xc_run = None
        self._init_toolset()

    def generate(self):
        save(
            self._conanfile,
            os.path.join(self.generators_folder, 'project-config.jam'),
            _pkg_config_template,
        )

        var_id = variation_id(self.variation)
        var_key = variation_key(var_id)

        toolchain_template = Template(
            _toolchain_template, trim_blocks=True, lstrip_blocks=True)
        save(
            self,
            os.path.join(
                self.generators_folder, f'conantoolchain-{var_key}.jam',
            ),
            toolchain_template.render(toolsets=self.toolsets),
        )

    def using(self, name, *args):
        self._toolsets[name] = args

    def _init_toolset(self):
        if self._conanfile.conf.get(
            'user.b2:toolset', default=None, check_type=str,
        ):
            return

        toolset = self.variation.get('toolset')
        if not toolset:
            return

        toolset = toolset.split('-')
        if len(toolset) > 1:
            toolset = ('-'.join(toolset[:-1]), toolset[-1])
        else:
            toolset = (toolset[0], None)

        build_env = Environment().vars(self._conanfile)

        compilers_by_conf = self._conanfile.conf.get(
            'tools.build:compiler_executables',
            default={},
            check_type=dict)

        def get_tool(var, apple_tool=None):
            result = build_env.get(var)
            if not result and apple_tool:
                result = self._get_apple_tool(var.lower())
            return result

        def get_flags(var, conf=None):
            result = [f for f in build_env.get(var, '').split(' ') if f]
            if conf:
                result += self._conanfile.conf.get(
                    f'tools.build:{conf}', default=[], check_type=list)
            return result

        def get_compiler(var, comp):
            return compilers_by_conf.get(comp) or build_env.get(var)

        opts = {}

        archiver = get_tool('AR')
        if archiver:
            opts['archiver'] = archiver

        ranlib = get_tool('RANLIB')
        if ranlib:
            opts['ranlib'] = ranlib

        strip = get_tool('STRIP')
        if strip:
            opts['striper'] = strip

        cxxflags = get_flags('CXXFLAGS', 'cxxflags')
        if cxxflags:
            opts['cxxflags'] = cxxflags

        cflags = get_flags('CFLAGS', 'cflags')
        if cflags:
            opts['cflags'] = cflags

        compileflags = get_flags('CPPLAGS')
        if compileflags:
            opts['compileflags'] = compileflags

        linkflags = get_flags('LDFLAGS', 'sharedlinkflags')
        if linkflags:
            opts['linkflags'] = linkflags

        arflags = get_flags('ARFLAGS')
        if arflags:
            opts['arflags'] = arflags

        asmflags = get_flags('ASMFLAGS')
        if asmflags:
            opts['asmflags'] = asmflags

        rc = get_compiler('RC', 'rc')
        if rc:
            key = 'resource-compiler' if toolset[0] == 'msvc' else 'rc'
            opts[key] = rc

        assembler = get_compiler('AS', 'asm')
        if assembler:
            opts['assembler'] = assembler

        command = get_compiler('CXX', 'cpp') or get_compiler('CC', 'c') or ''

        self.using(toolset, command, opts)

    def _get_apple_tool(self, name):
        if self._xc_run is None:
          if (is_apple_os(self._conanfile)
              and self._conanfile.settings.compiler == 'apple-clang'):
              self._xc_run = dict()
          else:
              self._xc_run = XCRun(self._conanfile)
        return getattr(self._xc_run, name)

    @property
    def toolsets(self):
        for k, v in self._toolsets.items():
            if isinstance(k, tuple):
                items = list(k)
            else:
                items = [k]
            items += [ self._toolset_param(param) for param in v ]
            items = [ x if x is not None else '' for x in items ]
            yield items

    def _toolset_param(self, param):
        if isinstance(param, collections.abc.Mapping):
            param = [
                self._mapping_item(k, v)
                for k, v in sorted(param.items())
                if v
            ]

        if (
            isinstance(param, collections.abc.Iterable)
            and not isinstance(param, str)
        ):
            param = ' '.join(param)

        return param

    def _mapping_item(self, key, value):
        key = jamify(key)
        pattern = '<{key}>"{value}"'
        if (
            isinstance(value, collections.abc.Iterable)
            and not isinstance(value, str)
        ):
            return ' '.join(
                (pattern.format(key=key, value=v) for v in value if v)
            )
        else:
            return pattern.format(key=key, value=value)


class B2Deps(object):
    def __init__(self, conanfile, generators_folder=None):
        self._conanfile = conanfile
        self.generators_folder = (
            generators_folder or conanfile.generators_folder
        )
        self.excluded_dependencies = [
            'bzip2',
            'libjpeg',
            'libpng',
            'libtiff',
            'openssl',
            'qt',
            'xz_utils',
            'zlib',
            'zstd',
        ]
        self._clear_cache()

    def generate(self):
        self._clear_cache()

        save(
            self._conanfile,
            os.path.join(self.generators_folder, 'project-config.jam'),
            _pkg_config_template,
        )

        save(
            self._conanfile,
            os.path.join(self.generators_folder, 'conandeps.jam'),
            _conandeps_template,
        )

        dependencies = (
            dep
            for require, dep in self._conanfile.dependencies.items()
            if require.direct or not require.build or not require.test
        )
        projects = self._collect_targets(dependencies)
        for project, pkgs in projects.items():
            for path, content in self._project_content(project, pkgs):
                save(self._conanfile, path, content)

    def _project_content(self, project, pkgs):
        for pkg in pkgs.values():
            self._conanfile.output.info(pkg['package'])
            if pkg['package'].ref.name in self.excluded_dependencies:
                return

        project_dir = os.path.join(
            self.generators_folder,
            'b2_dep' + project.replace('/', '-'),
        )

        yield os.path.join(project_dir, 'build.jam'), _dep_root_template

        entry_template = Template(
            _dep_entry_template, trim_blocks=True, lstrip_blocks=True)
        yield (
            os.path.join(project_dir, 'entry.jam'),
            entry_template.render(path=project_dir, project=project),
        )

        deps = set()
        for pkg_id, pkg in pkgs.items():
            targets = pkg['targets']
            yield (
                os.path.join(project_dir, f'id-{pkg_id}.jam'),
                Template(_dep_pkg_template).render(targets=targets),
            )

            for target in targets:
                deps.add(target['component'])

        for dep in deps:
            for src in dep.cpp_info.builddirs:
                if os.path.exists(src):
                    shutil.copytree(src, project_dir, dirs_exist_ok=True)

    def _clear_cache(self):
        self._targets = {}
        self._projects = {}

    def _collect_targets(self, dependencies):
        for dep in dependencies:
            self._collect_targets_for_package(dep)
        return self._projects

    def _collect_targets_for_package(self, dep):
        main_target = self._targets.get(dep.cpp_info)
        if main_target is not None:
            return main_target

        project, target_name = _b2_target(dep.ref.name, dep.cpp_info)
        var = variation(dep, self._conanfile)

        targets = _collect_targets_for_component(
            dep.cpp_info, dep, project, target_name, var
        )
        main_target = targets[0]
        self._targets[dep.cpp_info] = main_target

        project = self._projects.setdefault(project, {})
        pkg = project.setdefault(dep.pref.package_id, {})
        pkg['package'] = dep
        pkg_targets = pkg.setdefault('targets', [])
        pkg_targets.extend(targets)

        for name, comp in dep.cpp_info.components.items():
            project, target_name = _b2_target(name, comp)
            targets = _collect_targets_for_component(
                comp, dep, project, target_name, var,
            )
            comp_target = targets[0]
            self._targets[comp] = comp_target

            main_target['dependencies'].append(comp_target)
            project = self._projects.setdefault(project, {})
            pkg = project.setdefault(dep.pref.package_id, {})
            pkg['package'] = dep
            pkg_targets = pkg.setdefault('targets', [])
            pkg_targets.extend(targets)

        for comp in dep.cpp_info.components.values():
            comp_tgt = self._targets[comp]
            for pkg_name, req_name in comp.parsed_requires():
                if pkg_name is None:
                    req_comp = dep.cpp_info.components[req_name]
                else:
                    pkg = dep.dependencies[pkg_name]
                    self._collect_targets_for_package(pkg)
                    if req_name == pkg_name:
                        req_comp = pkg.cpp_info
                    else:
                        req_comp = pkg.cpp_info.components[req_name]
                comp_tgt['dependencies'].append(self._targets[req_comp])
        else:
            main_target['dependencies'].extend((
                self._collect_targets_for_package(other)
                for other in dep.dependencies.direct_host.values()
            ))

        return main_target


class B2(object):
    def __init__(
        self,
        conanfile,
        source_folder=None,
        build_folder=None,
        package_folder=None,
        generators_folder=None,
        project_config=None,
        user_config=None,
        site_config=None,
    ):
        self._conanfile = conanfile
        self.source_folder = source_folder or conanfile.source_folder
        self.build_folder = build_folder or conanfile.build_folder
        self.package_folder = package_folder or conanfile.package_folder
        self.generators_folder = (
            generators_folder or conanfile.generators_folder
        )
        self.project_config = project_config
        self.user_config = user_config or conanfile.conf.get(
            'user.b2:user_config', default=None, check_type=str,
        )
        self.site_config = site_config or conanfile.conf.get(
            'user.b2:site_config', default=None, check_type=str,
        )

        self.build_request = _collect_variations(conanfile)

    def build(self, target=None, args=[]):
        cmd = 'b2'
        if target:
            if isinstance(target, collections.abc.Iterable):
                if not isinstance(target, str):
                    target = ' '.join(target)
            else:
                target = str(target)
            cmd += ' ' + target

        project_config = self.project_config
        if project_config is None:
            path = os.path.join(self.generators_folder, 'project-config.jam')
            if os.path.exists(path):
                project_config = path
        if project_config:
            cmd += f' --project-config="{project_config}"'

        if self.user_config is not None:
            cmd += f' --user-config="{self.user_config}"'

        if self.site_config is not None:
            cmd += f' --user-config="{self.site_config}"'

        cmd += f' --build-dir="{self.build_folder}"'
        cmd += f' install-prefix="{self.package_folder}"'

        for feature, value in self.build_request.items():
            if value:
                cmd += f' {feature}="{value}"'

        if args:
            cmd += ' ' + ' '.join(args)

        with chdir(self, self.source_folder):
            self._conanfile.run(cmd)

    def install(self):
        self.build('install')


def variation(conanfile, consumer_conanfile):
    result = {
        'toolset': _toolset(conanfile, consumer_conanfile)
    }

    arch = conanfile.settings.get_safe('arch')

    result['architecture'] = {
        'x86': 'x86', 'x86_64': 'x86',
        'ppc64le': 'power', 'ppc64': 'power', 'ppc32': 'power', 'ppc32be': 'power',
        'armv4': 'arm', 'armv4i': 'arm',
        'armv5el': 'arm', 'armv5hf': 'arm',
        'armv6': 'arm', 'armv7': 'arm', 'armv7hf': 'arm', 'armv7s': 'arm', 'armv7k': 'arm',
        'armv8': 'arm', 'armv8_32': 'arm', 'armv8.3': 'arm',
        'sparc': 'sparc', 'sparcv9': 'sparc',
        'mips': 'mips1', 'mips64': 'mips64',
        's390': 's390', 's390x': 's390',
    }.get(arch)

    result['instruction-set'] = {
        'armv4': 'armv4',
        'armv6': 'armv6', 'armv7': 'armv7', 'armv7s': 'armv7s',
        'ppc64': 'powerpc64',
        'sparcv9': 'v9',
    }.get(arch)

    result['address-model'] = {
        'x86': '32', 'x86_64': '64',
        'ppc64le': '64', 'ppc64': '64', 'ppc32': '32', 'ppc32be': '32',
        'armv4': '32', 'armv4i': '32',
        'armv5el': '32', 'armv5hf': '32',
        'armv6': '32', 'armv7': '32', 'armv7s': '32', 'armv7k': '32', 'armv7hf': '32',
        'armv8': '64', 'armv8_32': '32', 'armv8.3': '64',
        'sparc': '32', 'sparcv9': '64',
        'mips': '32', 'mips64': '64',
        's390': '32', 's390x': '64',
    }.get(arch)

    result['target-os'] = {
        'Windows': 'windows', 'WindowsStore': 'windows', 'WindowsCE': 'windows',
        'Linux': 'linux',
        'Macos': 'darwin',
        'Android': 'android',
        'iOS': 'iphone',
        'watchOS': 'iphone',
        'tvOS': 'appletv',
        'FreeBSD': 'freebsd',
        'SunOS': 'solaris',
        'Arduino': 'linux',
        'AIX': 'aix',
        'VxWorks': 'vxworks',
    }.get(conanfile.settings.get_safe('os'))

    if (result['target-os'] == 'windows' and
            conanfile.settings.get_safe('os.subsystem') == 'cygwin'):
        result['target-os'] = 'cygwin'

    result['variant'] = {
        'Debug': 'debug',
        'Release': 'release',
        'RelWithDebInfo': 'relwithdebinfo',
        'MinSizeRel': 'minsizerel',
    }.get(conanfile.settings.get_safe('build_type'))

    cppstd = conanfile.settings.get_safe('compiler.cppstd')

    result['cxxstd'] = {
        '98': '98', 'gnu98': '98',
        '11': '11', 'gnu11': '11',
        '14': '14', 'gnu14': '14',
        '17': '17', 'gnu17': '17',
        '20': '20', 'gnu20': '20',
        '23': '23', 'gnu23': '23',
        '26': '26', 'gnu26': '26',
        '2a': '2a', 'gnu2a': '2a',
        '2b': '2b', 'gnu2b': '2b',
        '2c': '2c', 'gnu2c': '2c',
    }.get(cppstd)

    if cppstd and cppstd.startswith('gnu'):
        result['cxxstd-dialect'] = 'gnu'

    libcxx = conanfile.settings.get_safe('compiler.libcxx')
    if libcxx:
        stdlibs = {
            'libstdc++': 'gnu',
            'libstdc++11': 'gnu11',
            'libc++': 'libc++',
        }
        if conanfile.settings.get_safe('compiler') == 'sun-cc':
            stdlibs.update(
                libstdcxx='apache',
                libstlport='sun-stlport'
            )
        result['stdlib'] = stdlibs.get(libcxx)

    threads = conanfile.settings.get_safe('compiler.threads')
    if threads:
        result['threadapi'] = {
            'posix': 'pthread',
            'win32': 'win32',
        }.get(threads)

    runtime = conanfile.settings.get_safe('compiler.runtime')
    if runtime:
        result['runtime-link'] = {
            'static': 'static',
            'MT': 'static',
            'MTd': 'static',
            'dynamic': 'shared',
            'MD': 'shared',
            'MDd': 'shared',
        }.get(runtime)
        result['runtime-debugging'] = {
            'Debug': 'on',
            'MTd': 'on',
            'MDd': 'on',
            'Release': 'off',
            'MT': 'off',
            'MD': 'off',
        }.get(conanfile.settings.get_safe('compiler.runtime_type') or runtime)

    link = conanfile.options.get_safe('shared')
    if link is not None:
        result['link'] = 'shared' if link else 'static'

    return result

def _collect_variations(conanfile):
    result = {}
    packages = [
        dep
        for require, dep in conanfile.dependencies.items()
        if require.direct or not require.build or not require.test
    ] + [conanfile]
    for pkg in packages:
        for k, v in variation(pkg, conanfile).items():
            if v is None:
                continue
            old = result.get(k)
            if old is not None and old != v:
                if v.startswith(old):
                    result[k] = v
                elif not old.startswith(v):
                    raise Exception(f'incompatible values for {k}: {old}, {v}')
            else:
                result[k] = v
    return result

def variation_id(variation):
    return ','.join((i[1] for i in _nonempty_items(variation)))


def variation_key(variation_id):
    return md5(variation_id.encode('utf-8')).hexdigest()

def jamify(s):
    lowered = ''
    for c in s:
        if c.isupper():
            lowered += '-'
            lowered += c.lower()
        else:
            lowered += c
    if lowered.startswith('-'):
        lowered = lowered[1:]
    return lowered.replace('_', '-')


def _nonempty_items(variation):
    return (i for i in sorted(variation.items()) if i[1])


def _toolset(conanfile, consumer_conanfile):
    toolset = consumer_conanfile.conf.get(
        'user.b2:toolset', default=None, check_type=str,
    )
    if toolset:
        return toolset

    compiler = conanfile.settings.get_safe('compiler')
    toolset = {
        'sun-cc': 'sun',
        'gcc': 'gcc',
        'Visual Studio': 'msvc',
        'msvc': 'msvc',
        'clang': 'clang',
        'apple-clang': 'clang'
    }.get(compiler)
    if not toolset:
        return

    version = conanfile.settings.get_safe('compiler.version')
    if version:
        if toolset == 'msvc':
            visual_studio_version = msvc_version_to_vs_ide_version(version)
            version = {
                '15': '14.1',
                '16': '14.2',
                '17': '14.3',
            }.get(visual_studio_version) or (visual_studio_version + '.0')
        return toolset + '-' + version

    return toolset


def _b2_target(name, info):
    project = None
    target = info.get_property('b2_target_name', check_type=str)
    if target:
        target = target.split('//')
        if len(target) > 1:
            project = target[0]
        target = target[-1]

    if not target:
        target = info.get_property(
            'cmake_target_name', check_type=str,
        ) or ''
        target = [ jamify(part) for part in target.split(sep='::') ]
        if len(target) > 1:
            project = '/'.join(target[:-1])
        target = target[-1]

    if not project:
        project = '/' + jamify(name)

    if not target:
        target = 'libs'

    return project, target


def _collect_targets_for_component(info, pkg, project, name, variation):
    libs = [
        _lib_target(project, lib, info, pkg, variation) for lib in info.libs
    ]

    if len(libs) == 1:
        main_target = libs[0]
        main_target['name'] = name
        libs = []
    elif not libs:
        main_target = _alias_target(project, name, info, pkg, variation)
    else:
        main_target = _simple_alias_target(project, name, pkg, var)
        main_target['dependencies'].extend(libs)

    return [main_target] + libs


def _lib_target(project, name, info, pkg, var):
    result = _alias_target(project, name, info, pkg, var)
    libs = []
    for dir in info.libdirs:
        libs += glob.glob(os.path.join(dir, f'*{name}*'))
    libs = sorted(libs, key=lambda lib: len(lib))
    result.update(
        kind='lib',
        lib_name=name,
        search=info.libdirs,
        file=libs[0],
    )
    return result


def _alias_target(project, name, info, pkg, var):
    result = _simple_alias_target(project, name, pkg, var)
    linkflags = info.sharedlinkflags or []
    linkflags.extend(info.exelinkflags or [])
    result.update(
        includes=info.includedirs,
        defines=info.defines,
        cflags=info.cflags,
        cxxflags=info.cxxflags,
        linkflags=linkflags,
    )
    return result


def _simple_alias_target(project, name, pkg, var):
    return {
        'project': project,
        'name': name,
        'kind': 'alias',
        'variation': var,
        'component': pkg,
        'dependencies': [],
    }


_toolchain_template = '''\
# Conan automatically generated config file
# DO NOT EDIT MANUALLY, it will be overwritten

{% for toolset in toolsets %}
using {{ toolset | join(' : ') }} ;
{% endfor %}
'''

_pkg_config_template = '''\
# Conan automatically generated config file
# DO NOT EDIT MANUALLY, it will be overwritten

import feature ;
import modules ;
if ! ( relwithdebinfo in [ feature.values variant ] )
{
    variant relwithdebinfo : : <optimization>speed <debug-symbols>on <inlining>full <runtime-debugging>off ;
}
if ! ( minsizerel in [ feature.values variant ] )
{
    variant minsizerel : : <optimization>space <debug-symbols>off <inlining>full <runtime-debugging>off ;
}

local GENERATORS_FOLDER = [ modules.binding $(__name__) ] ;
GENERATORS_FOLDER = $(GENERATORS_FOLDER:D) ;
for local file in [ glob conan*.jam ]
{
    include $(GENERATORS_FOLDER)/$(file) ;
}
'''

_conandeps_template = '''\
# Conan automatically generated config file
# DO NOT EDIT MANUALLY, it will be overwritten

import modules ;
import path ;

local GENERATORS_FOLDER = [ modules.binding $(__name__) ] ;
GENERATORS_FOLDER = [ path.make $(GENERATORS_FOLDER:D) ] ;
for local dep in [ glob $(GENERATORS_FOLDER)/b2_dep-*/entry.jam ]
{
    include [ path.native [ path.root $(dep) $(GENERATORS_FOLDER) ] ] ;
}
'''

_dep_entry_template = '''\
# Conan automatically generated config file
# DO NOT EDIT MANUALLY, it will be overwritten
import path ;
project-search {{ project }} : [ path.make "{{ path | replace('\\\\', '\\\\\\\\') }}" ] ;
'''

_dep_root_template = '''\
# Conan automatically generated config file
# DO NOT EDIT MANUALLY, it will be overwritten
path-constant here : . ;
for local var in [ glob id-*.jam ]
{
    include $(here)/$(var) ;
}

'''

_dep_pkg_template = '''\
# Conan automatically generated config file
# DO NOT EDIT MANUALLY, it will be overwritten

# temporary hack
project
    : common-requirements
{% for target in targets %}
    {% for dir in target.includes %}
      <include>"{{ dir | replace('\\\\', '\\\\\\\\') }}"
    {% endfor %}
{% endfor %}
    ;

{% for target in targets %}

{{ target.kind }} {{ target.name }}
    :
    {% if target.kind == 'alias' %}
    {% for src in target.dependencies %}
        {% if src.project != target.project %}{{ src.project }}//{% endif %}{{ src.name }}
    {% endfor %}
    {% endif %}
    :
    {% if target.kind == 'lib' and target.search %}
        <file>"{{ target.file | replace('\\\\', '\\\\\\\\') }}"
    {% endif %}
    {% for feature, value in target.variation.items() %}
        {% if value %}<{{ feature }}>"{{ value }}"{% endif %}
    {% endfor %}
    :
    :
    {% for dir in target.includes %}
        <include>"{{ dir | replace('\\\\', '\\\\\\\\') }}"
    {% endfor %}
    {% for define in target.defines %}
        <define>"{{ define }}"
    {% endfor %}
    {% for flag in target.cflags %}
        <cflags>"{{ flag }}"
    {% endfor %}
    {% for flag in target.cxxflags %}
        <cxxflags>"{{ flag }}"
    {% endfor %}
    {% for flag in target.linkflags %}
        <linkflags>"{{ flag }}"
    {% endfor %}
    {% if target.kind == 'lib' %}
    {% for src in target.dependencies %}
        <library>{% if src.project != target.project %}{{ src.project }}//{% endif %}{{ src.name }}
    {% endfor %}
    {% endif %}
    ;

{% endfor %}
'''
