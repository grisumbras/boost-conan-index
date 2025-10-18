import glob
import os.path
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import (
    copy,
    rmdir,
    save,
)
from conan.tools.scm import Git

class BoostPoolRecipe(ConanFile):
    name = 'boost-pool'

    license = 'BSL-1.0'
    description = '''Memory pool management.'''
    author = 'Steve Cleary'
    url = 'https://github.com/boostorg/pool.git'
    topics = ['Memory']

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

    def build(self):
        build_jam = os.path.join(self.source_folder, 'build.jam')
        if not glob.glob(build_jam):
            with open(build_jam, 'w') as f:
                f.write(_build_jam)

        b2 = self.python_requires['b2-tools'].module.B2(self)
        b2.build('boost_pool')

    def package(self):
        b2 = self.python_requires['b2-tools'].module.B2(self)
        b2.build(target='conan-install')

    def package_info(self):
        self.cpp_info.set_property('cmake_target_name', 'Boost::pool')
        self.cpp_info.set_property('b2_target_name', '/boost/pool//boost_pool')

        if self._is_header_only:
            self.cpp_info.bindirs = []
            self.cpp_info.libdirs = []
        else:
            self.cpp_info.libs = ['boost_pool']
            self.cpp_info.defines = ['BOOST_POOL_NO_LIB=1']
        self.cpp_info.resdirs = ['share']
        self.cpp_info.builddirs = ['share/boost/pool/modules']

    def package_id(self):
        if self._is_header_only:
            self.info.clear()

    @property
    def _data_cache(self):
        result = getattr(self, '_conan_data', None)
        if result is None:
            result = self.conan_data['sources'][self.version]
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

'''

_build_jam = '''\
require-b2 5.3.0 ;

project /boost/pool ;

alias boost_pool : : : <include>include ;

call-if : boost-library pool ;
'''