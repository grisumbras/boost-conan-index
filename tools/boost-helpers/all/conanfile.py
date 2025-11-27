#
# Copyright (c) 2025 Dmitry Arkhipov (grisumbras@yandex.ru)
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#


import glob
import os.path
import shutil
from conan import ConanFile
from conan.errors import ConanException
from conan.tools.build import check_min_cppstd
from conan.tools.files import (
    collect_libs,
    copy,
    load,
    mkdir,
    patch,
    rename,
    rmdir,
    save,
)
from conan.tools.scm import Git
from jinja2 import Template
import yaml


class BoostHelpersRecipe(ConanFile):
    name = 'boost-helpers'
    description = 'Recipe tools for Boost packages'
    author = 'Dmitry Arkhipov'
    url = 'https://grisumbras/boost-conan-index'
    license = 'BSL-1.0'
    package_type = 'python-require'
    exports = 'LICENSE_1_0.txt', 'data.yml'


class BoostPackage():
    def configure(self):
        if self._is_header_only:
            self.settings.rm_safe('os')
            self.settings.rm_safe('build_type')
            self.settings.rm_safe('arch')

            if not self._data_cache['cxxstd']:
                self.settings.rm_safe('compiler')
            else:
                for k, _ in self.settings.compiler.values_list:
                    if k in ('compiler', 'compiler.cppstd'):
                        continue
                    self.settings.rm_safe(k)

    def configure_options(self):
        if self._is_header_only:
            del self.options.shared

    def validate(self):
        cxxstd = self._data_cache['cxxstd']
        if cxxstd:
            check_min_cppstd(self, cxxstd)

    def requirements(self):
        for dep in self._data_cache['dependencies']:
            self.requires(
                dep['ref'],
                headers=True,
                transitive_headers=dep['public'],
                libs=not dep['header'] and not self._is_header_only,
                transitive_libs=dep['public'] and not dep['header'],
            )

    def build_requirements(self):
       self.tool_requires(f'b2/[>={self._b2_version}]')

    def layout(self):
        self.folders.build = 'bin.v2'
        self.folders.generators = 'bin.v2/generators'

    def source(self):
        git = Git(self)
        git.fetch_commit(self._data_cache['url'], self._data_cache['commit'])
        rmdir(self, '.git')

        build_jam = os.path.join(self.source_folder, 'build.jam')
        if not os.path.exists(build_jam):
            lib_jam_template = Template(
                _build_jam, trim_blocks=True, lstrip_blocks=True,
            )
            save(self, build_jam, lib_jam_template.render(conanfile=self))

        if not glob.glob(f'{self.source_folder}/LICENSE*'):
            copy(
                self,
                'LICENSE_1_0.txt',
                self.python_requires['b2-tools'].path,
                self.source_folder,
            )

        files = glob.glob('*')
        lib_dir = os.path.join(self.source_folder, 'libs', self.name[6:])
        mkdir(self, lib_dir)
        for file in files:
            rename(self, file, os.path.join(lib_dir, file))

        jamroot_template = Template(
            _jamroot, trim_blocks=True, lstrip_blocks=True)
        save(
            self,
            os.path.join(self.source_folder, 'build.jam'),
            jamroot_template.render(conanfile=self),
        )

    def generate(self):
        b2_gens = self.python_requires['b2-tools'].module

        tc = b2_gens.B2Toolchain(self)
        if self.name == 'boost-mpi':
            tc.using('mpi')
        tc.generate()

        deps = b2_gens.B2Deps(self)
        deps.generate()

        save(
            self,
            os.path.join(self.generators_folder, 'conanboost.jam'),
            _boost_install,
        )

        libs_dir = os.path.join(self.source_folder, 'libs')
        if (os.path.exists(libs_dir)
            and ('boost-config' in self.dependencies.direct_host)
        ):
            config_dir = os.path.join(libs_dir, 'config')
            boost_config = self.dependencies['boost-config']
            for src in boost_config.cpp_info.builddirs:
                if os.path.exists(src):
                    shutil.copytree(src, config_dir)

        if 'boost-predef' in self.dependencies.direct_host:
            patch(self, patch_string=_predef_patch, fuzz=True)

    def build(self):
        b2 = self.python_requires['b2-tools'].module.B2(self)
        libs = [
            f'libs/{self.name[6:]}//{tgt["name"]}'
            for tgt in self._data_cache['libraries']
        ]
        if libs:
            b2.build(libs)

    def package(self):
        requested = [tgt['name'] for tgt in self._data_cache['libraries']]
        args = ['--requested-libraries=' + ','.join(requested)]

        b2 = self.python_requires['b2-tools'].module.B2(self)
        b2.build(f'libs/{self.name[6:]}//conan-install', args=args)

        lib_name = self.name[6:]
        targets_file = os.path.join(
            self.package_folder, 'share', 'boost', lib_name, 'targets.yml',
        )
        actual_targets = yaml.load(load(self, targets_file), yaml.Loader)
        for target in self._data_cache['libraries']:
            name = target['name']
            if name not in actual_targets:
                raise ConanException(f'Target {name} was not installed')

            actual = actual_targets[name]
            kind = 'library' if actual.get('files', []) else 'header-library'
            if target['kind'] != kind:
                raise ConanException(
                    f'Target {name} has the wrong kind\n'
                    f'  expected: {target["kind"]}, got: {kind}'
                )

    def package_info(self):
        lib_name = self.name[6:]

        self.cpp_info.bindirs = []
        self.cpp_info.resdirs = ['share']
        self.cpp_info.builddirs = [f'share/boost/{lib_name}/modules']

        targets = self._data_cache['targets']
        no_autolink = [f'BOOST_{lib_name.upper()}_NO_LIB=1']

        if len(targets) < 2:
            self.cpp_info.set_property(
                'cmake_target_name', f'Boost::{lib_name}',
            )
            self.cpp_info.set_property(
                'b2_target_name',
                f'/boost/{lib_name}//boost_{lib_name}',
            )

            if self._is_header_only:
                self.cpp_info.libdirs = []
            else:
                self.cpp_info.libs = [
                    tgt['name'] for tgt in targets
                    if tgt['kind'] == 'library'
                ]
                self.cpp_info.defines = no_autolink
        else:
            self.cpp_info.set_property(
                'b2_target_name', f'/boost/{lib_name}//libs',
            )

            targets_file = os.path.join(
                self.package_folder, 'share', 'boost', lib_name, 'targets.yml',
            )
            actual_targets = yaml.load(load(self, targets_file), yaml.Loader)
            actual_targets = self._filtered_target_files(actual_targets)

            for tgt in targets:
                name = tgt['name']
                actual_target = actual_targets[name]
                comp = self.cpp_info.components[name]
                comp.bindirs = []
                comp.set_property('cmake_target_name', 'Boost::' + name[6:])
                comp.set_property(
                    'b2_target_name',
                    f'/boost/{lib_name}//{name}',
                )
                if tgt['kind'] == 'library':
                    comp.libs = actual_target.get('files', [])
                    comp.defines = no_autolink
                else:
                    comp.libdirs = []
                comp.requires = [dep for dep in tgt['dependencies']]
                for dep in self._data_cache['dependencies']:
                    dep_name = dep['ref'].split('/')[0]
                    comp.requires.append(dep_name + '::' + dep_name)

    def package_id(self):
        if self._is_header_only:
            self.info.clear()
        else:
            self.info.options.rm_safe('disabled_libraries')
            self.info.libraries = ';'.join([
                tgt['name'] for tgt in self._data_cache['libraries']
            ])

    @property
    def _data_cache(self):
        result = getattr(self, '_conan_data', None)
        if result is None:
            result = self.conan_data['sources'][self.version]

            disabled_libs = str(self.options.disabled_libraries).split(',')

            targets = []
            libraries = []
            for target in result['targets']:
                name = target['name']
                if target['kind'] == 'library':
                    if name not in disabled_libs:
                        libraries.append(target)
                        targets.append(target)
                else:
                    targets.append(target)

            if not targets:
                targets.append({
                    'name': 'boost_' + self.name[6:],
                    'kind': 'header-library',
                    'dependencies': [],
                })

            result['targets'] = targets
            result['libraries'] = libraries
            result['kind'] = 'library' if libraries else 'header-library'

            base = self.python_requires['boost-helpers']
            data = yaml.load(
                load(self, os.path.join(base.path, 'data.yml')),
                yaml.Loader,
            )
            result.update(data)

            self._conan_data = result

        return result

    @property
    def _is_header_only(self):
        return self._data_cache['kind'] == 'header-library'

    @property
    def _b2_version(self):
        return self._data_cache['b2_version']

    def _filtered_target_files(self, targets):
        found_libs = set(collect_libs(self))

        for target in targets.values():
            files = target.get('files', [])
            matched_libs = []
            for lib in found_libs:
                for file in files:
                    if lib in file:
                        matched_libs.append(lib)
                        break

            if len(matched_libs) > 1:
                preferred_lib = None
                max_len = 0
                for lib in matched_libs:
                    cur_len = len(lib)
                    if cur_len > max_len:
                        preferred_lib = lib
                        max_len = cur_len
                matched_libs = [preferred_lib]

            if files and not matched_libs:
                raise ConanException(
                    'None of the found libraries matches files:' +
                    ', '.join(files)
                )

            if matched_libs:
                found_libs.remove(matched_libs[0])
                target['files'] = matched_libs

        return targets


_boost_install = '''\
# Conan automatically generated config file
# DO NOT EDIT MANUALLY, it will be overwritten

import option ;
import print ;
import project ;
import property ;
import property-set ;
import regex ;
import virtual-target ;

rule conan-install ( id : libraries * )
{
    local p = [ project.current ] ;
    if [ $(p).has-alternative-for-target conan-install ]
    {
        return ;
    }

    for local lib in $(libraries)
    {
        install conan-install-$(lib)
            : $(lib)
            : <location>(libdir)
              <install-type>STATIC_LIB
              <install-type>SHARED_LIB
              <install-type>PDB
            ;
        $(p).mark-target-as-explicit conan-install-$(lib) ;

        generate conan-$(lib)-info
            : $(lib)
            : <generating-rule>@conan-target-info
              <flags>target=$(lib)
            ;
        $(p).mark-target-as-explicit conan-$(lib)-info ;
    }

    local lib_name = $(id) ;

    id = /boost/$(id) ;

    local requested = [ option.get requested-libraries ] ;
    if $(requested)
    {
        libraries = [ regex.split $(requested:E=) , ] ;
    }
    else
    {
        libraries = ;
    }

    make targets.yml
        : conan-$(libraries)-info
        : @make-libraries-info
        : <flags>project=$(lib_name)
        ;
    $(p).mark-target-as-explicit targets.yml ;

    install install-targets-info
        : targets.yml
        : <location>"(datarootdir)$(id)"
        ;
    $(p).mark-target-as-explicit install-targets-info ;

    alias conan-install-libraries
        : conan-install-$(libraries)
          install-targets-info
        ;

    install conan-install-headers
        : [ glob-tree-ex include : *.* ]
        : <location>(includedir)
          <install-source-root>include
        ;
    $(p).mark-target-as-explicit conan-install-headers ;

    install conan-install-license
        : [ glob LICENSE* ]
        : <location>"(datarootdir)$(id)"
        ;
    $(p).mark-target-as-explicit conan-install-license ;

    install conan-install-jam
        : [ glob *.jam : build.jam ]
          [ glob-tree-ex checks check tools : *.* ]
        : <location>"(datarootdir)$(id)/modules"
          <install-source-root>.
        ;
    $(p).mark-target-as-explicit conan-install-jam ;

    alias conan-install
        : conan-install-libraries
          conan-install-headers
          conan-install-license
          conan-install-jam
        ;
    $(p).mark-target-as-explicit conan-install ;
}

rule conan-target-info ( project name : property-set : sources * )
{
    local target ;
    for local flag in [ $(property-set).get <flags> ]
    {
        local match = [ MATCH (.*)=(.*) : $(flag) ] ;
        if "$(match[1])" = target
        {
            if $(sources)
            {
                target = $(match[2])/$(sources:J=/) ;
            }
            else
            {
                target = $(match[2]) ;
            }
        }
    }

    return [ property-set.create <flags>target=$(target) ] ;
}

rule make-libraries-info ( target : : props * )
{
    print.output $(target) ;

    local targets ;
    local project ;
    for local flag in [ property.select <flags> : $(props) ]
    {
        local match = [ MATCH (.*)=(.*) : $(flag:G=) ] ;
        if "$(match[1])" = target
        {
            local target = [ regex.split "$(match[2])" / ] ;
            local files ;
            for local src in $(target[2-])
            {
                files += [ $(src).name ] ;
            }
            files ?= "" ;
            target = $(target[0]) ;
            print.text "$(target):" "  files: [$(files:J=,)]" : overwrite ;
            targets += "$(target)" ;
        }
        else
        {
            if "$(match[1])" = project
            {
                project = "$(match[2])" ;
            }
        }
    }

    if ! ( boost_$(project) in $(targets) )
    {
        print.text "boost_$(project):" "  files: []" : overwrite ;
    }

    print.text "" : overwrite ;
}

rule boost-library ( id ? : options * : * )
{
    for n in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
    {
        local opt = $($(n)) ;
        if $(opt[1]) = install
        {
            conan-install $(id) : $(opt[2-]) ;
            if $(opt[1]) = install
            {
                called-conan-install = true ;
            }
        }
        if ! $(called-conan-install)
        {
            conan-install $(id) ;
        }
    }
}

constant BOOST_JAMROOT_MODULE : $(__name__) ;
rule tag ( name : type ? : property-set )
{
    return [ virtual-target.add-prefix-and-suffix $(name) : $(type)
        : $(property-set) ] ;
}

'''

_build_jam = '''\
require-b2 {{ conanfile._b2_version }} ;

project
    : requirements
{% if not conanfile._is_header_only %}
    {% for req, dep in conanfile.dependencies.items() %}
        {% if req.direct and dep.ref.name.startswith('boost-') %}
            <library>/boost/{{dep.ref.name[6:]}}//boost_{{dep.ref.name[6:]}}
        {% endif %}
    {% endfor %}
            <include>include
{% endif %}
    ;

alias {{ conanfile.name | replace('-', '_') }}
{% if conanfile._is_header_only %}
    : : : <include>include ;
{% else %}
    : build//{{ conanfile.name | replace('-', '_') }} ;
{% endif %}

call-if : boost-library {{ conanfile.name[6:] }}
{% if conanfile._is_header_only %}
    ;
{% else %}
    : install {{ conanfile.name | replace('-', '_') }} ;
{% endif %}
'''

_jamroot = '''\
require-b2 {{ conanfile._b2_version }} ;

project boost ;

rule boost-install ( * ) { }
'''

_predef_patch = '''\
--- a/bin.v2/generators/b2_dep-boost-predef/tools/check/predef.jam
+++ b/bin.v2/generators/b2_dep-boost-predef/tools/check/predef.jam
@@ -16,9 +16,6 @@ import path ;
 import "class" : new ;
 import regex ;

-# Create a project for our targets.
-project.extension predef check ;
-
 # Feature to pass check expressions to check programs.
 feature.feature predef-expression : : free ;

@@ -30,9 +27,11 @@ rule check ( expressions + : language ? : true-properties * : false-properties *
     # Default to C++ on the check context.
     language ?= cpp ;
     \n\
-    local project_target = [ project.target $(__name__) ] ;
+    local binding = [ modules.binding $(__name__) ] ;
+    local mod = [ project.find $(binding:D) : $(binding) ] ;
+    local project_target = [ project.target $(mod) ] ;
     $(project_target).reset-alternatives ;
-\tproject.push-current $(project_target) ;
+    project.push-current $(project_target) ;
     local terms ;
     local result ;
     for expression in $(expressions)
@@ -48,11 +47,11 @@ rule check ( expressions + : language ? : true-properties * : false-properties *
             if ! ( $(key) in $(_checks_) )
             {
                 _checks_ += $(key) ;
-                _message_(/check/predef//predef_check_cc_$(key)) = $(expression) ;
+                _message_($(binding:D)//predef_check_cc_$(key)) = $(expression) ;
                 check_target $(language) $(key) : [ change_term_to_def $(expression) ] ;
             }
             \n\
-            terms += /check/predef//predef_check_cc_$(key) ;
+            terms += $(binding:D)//predef_check_cc_$(key) ;
         }
     }
     local instance = [ new check-expression-evaluator
@@ -118,7 +117,8 @@ local rule check_target ( language key : requirements * )
     obj predef_check_cc_$(key)
         : $(source_path)
         : <include>$(include_path) $(requirements) ;
-    explicit predef_check_cc_$(key) ;
+    local p = [ project.current ] ;
+    $(p).mark-target-as-explicit predef_check_cc_$(key) ;
     return predef_check_cc_$(key) ;
 }
 '''
