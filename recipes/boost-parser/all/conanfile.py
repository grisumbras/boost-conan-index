import glob
import os.path
import shutil
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import (
    copy,
    mkdir,
    rename,
    rmdir,
    save,
)
from conan.tools.scm import Git
from jinja2 import Template

class BoostParserRecipe(ConanFile):
    name = 'boost-parser'

    license = 'BSL-1.0'
    description = '''A parser combinator library.'''
    author = 'T. Zachary Laine'
    url = 'https://github.com/boostorg/parser.git'
    topics = ['Parsing']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = 'b2-tools/0.0.1-a'

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
       self.tool_requires('b2/[>=5.3.0]')

    def layout(self):
        self.folders.build = 'bin.v2'
        self.folders.generators = 'bin.v2/generators'

    def source(self):
        git = Git(self)
        git.fetch_commit(self._data_cache['url'], self._data_cache['commit'])
        rmdir(self, '.git')

        build_jam = os.path.join(self.source_folder, 'build.jam')
        if not glob.glob(build_jam):
            if self._is_header_only:
                save(self, build_jam, _build_jam)
            else:
                files = glob.glob('*')
                lib_dir = os.path.join(self.source_folder, 'libs', 'parser')
                mkdir(self, lib_dir)
                for file in files:
                    rename(self, file, os.path.join(lib_dir, file))

                save(self, build_jam, _jamroot)

                lib_jam_template = Template(
                    _lib_jam, trim_blocks=True, lstrip_blocks=True)
                save(
                    self,
                    os.path.join(self.source_folder, 'libs', 'build.jam'),
                    lib_jam_template.render(conanfile=self),
                )

        if not glob.glob(f'{self.source_folder}/LICENSE*'):
            copy(
                self,
                'LICENSE_1_0.txt',
                self.python_requires['b2-tools'].path,
                self.source_folder,
            )

    def generate(self):
        b2_gens = self.python_requires['b2-tools'].module

        tc = b2_gens.B2Toolchain(self)
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
            self.output.info(boost_config.cpp_info.builddirs)
            for src in boost_config.cpp_info.builddirs:
                if os.path.exists(src):
                    self.output.info(src)
                    shutil.copytree(src, config_dir)

    def build(self):
        b2 = self.python_requires['b2-tools'].module.B2(self)
        b2.build('boost_parser')

    def package(self):
        b2 = self.python_requires['b2-tools'].module.B2(self)
        b2.build(target='conan-install')

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.resdirs = ['share']
        self.cpp_info.builddirs = ['share/boost/parser/modules']

        targets = self._data_cache['targets']
        no_autolink = ['BOOST_PARSER_NO_LIB=1']

        if len(targets) < 2:
            self.cpp_info.set_property('cmake_target_name', 'Boost::parser')
            self.cpp_info.set_property('b2_target_name', '/boost/parser//boost_parser')

            if self._is_header_only:
                self.cpp_info.libdirs = []
            else:
                self.cpp_info.libs = [
                    'boost_' + tgt['name'] for tgt in targets
                    if tgt['kind'] == 'library'
                ]
                self.cpp_info.defines = no_autolink
        else:
            self.cpp_info.set_property('b2_target_name', '/boost/parser//libs')
            for tgt in targets:
                name = tgt['name']
                comp = self.cpp_info.components[name]
                comp.bindirs = []
                comp.set_property('cmake_target_name', 'Boost::' + name)
                comp.set_property('b2_target_name', '/boost/parser//boost_' + name)
                if tgt['kind'] == 'library':
                    comp.libs = ['boost_' + name]
                    comp.defines = no_autolink
                else:
                    comp.libdirs = []
                comp.requires = tgt['dependencies']
                for dep in self._data_cache['dependencies']:
                    dep_name = dep['ref'].split('/')[0]
                    comp.requires.append(dep_name + '::' + dep_name)

    def package_id(self):
        if self._is_header_only:
            self.info.clear()

    @property
    def _data_cache(self):
        result = getattr(self, '_conan_data', None)
        if result is None:
            result = self.conan_data['sources'][self.version]
            header_only = True
            for tgt in result['targets']:
                if tgt['kind'] == 'library':
                    header_only = False
                    break
            result['kind'] = 'header-library' if header_only else 'library'
            self._conan_data = result
        return result

    @property
    def _is_header_only(self):
        return self._data_cache['kind'] == 'header-library'


_boost_install = '''\
# Conan automatically generated config file
# DO NOT EDIT MANUALLY, it will be overwritten

import notfile ;
import project ;
import targets ;
import virtual-target ;

rule conan-install ( libraries * )
{
    local p = [ project.current ] ;
    if [ $(p).has-alternative-for-target conan-install ]
    {
        return ;
    }

    if $(libraries)
    {
        install conan-install-libraries-unchecked
            : $(libraries)
            : <location>(libdir)
              <install-type>STATIC_LIB
              <install-type>SHARED_LIB
              <install-type>PDB
            ;
        $(p).mark-target-as-explicit conan-install-libraries-unchecked ;
        targets.create-metatarget check-files-target-class
            : $(p)
            : conan-install-libraries
            : conan-install-libraries-unchecked
            : <action>@check-files-installed
            ;
    }
    else
    {
        alias conan-install-libraries ;
    }
    $(p).mark-target-as-explicit conan-install-libraries ;

    install conan-install-headers
        : [ glob-tree-ex include : *.* ]
        : <location>(includedir)
          <install-source-root>include
        ;
    $(p).mark-target-as-explicit conan-install-headers ;

    local id = [ $(p).get id ] ;
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

rule check-files-installed ( tgt : files * : props * )
{
    if ! $(files)
    {
        import errors ;
        errors.user-error No binaries were installed. ;
    }
}

rule boost-library ( id ? : options * : * )
{
    for n in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
    {
        local option = $($(n)) ;
        if $(option[1]) = install
        {
            conan-install $(option[2-]) ;
            if $(option[1]) = install
            {
                called-conan-install = true ;
            }
        }
        if ! $(called-conan-install)
        {
            conan-install ;
        }
    }
}

class check-files-target-class : make-target-class
{
    rule skip-from-usage-requirements ( ) { }
}

constant BOOST_JAMROOT_MODULE : $(__name__) ;
rule tag ( name : type ? : property-set )
{
    return [ virtual-target.add-prefix-and-suffix $(name) : $(type)
        : $(property-set) ] ;
}

'''

_build_jam = '''\
require-b2 5.3.0 ;

project /boost/parser ;

alias boost_parser : : : <include>include ;

call-if : boost-library parser ;
'''

_jamroot = '''\
require-b2 5.3.0 ;

project boost ;

rule boost-install ( libs * ) { conan-install $(libs) ; }

alias boost_parser : libs/parser/build//boost_parser ;

install conan-install-headers
    : [ glob-tree-ex libs/parser/include : *.* ]
    : <location>(includedir)
      <install-source-root>libs/parser/include
    ;
alias conan-install : libs/parser/build//conan-install conan-install-headers ;
explicit conan-install conan-install-headers ;
'''


_lib_jam = '''\
project
    : requirements
{% for req, dep in conanfile.dependencies.items() %}
    {% if req.direct and dep.ref.name.startswith('boost-') %}
        <library>/boost/{{dep.ref.name[6:]}}//boost_{{dep.ref.name[6:]}}
    {% endif %}
        <include>{{conanfile.name[6:]}}/include
{% endfor %}
    ;
'''
