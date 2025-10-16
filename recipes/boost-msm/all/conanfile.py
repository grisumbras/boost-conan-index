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

class BoostMsmRecipe(ConanFile):
    name = 'boost-msm'

    license = 'BSL-1.0'
    description = '''A very high-performance library for expressive UML2 finite state machines.'''
    author = 'Christophe Henry'
    url = 'https://github.com/boostorg/msm.git'
    topics = ['State']

    python_requires = 'b2-tools/0.0.1-a'
    package_type = 'header-library'
    settings = 'compiler'

    def validate(self):
        check_min_cppstd(self, '03')

    def requirements(self):
        deps = self.conan_data['sources'][self.version]['dependencies']
        for dep in deps['public']:
            self.requires(
                dep,
                headers=True,
                transitive_headers=True,
            )
        for dep in deps['private']:
            self.requires(
                dep,
                headers=True,)

    def build_requirements(self):
       self.tool_requires('b2/[>=5.3.0]')

    def layout(self):
        self.folders.build = 'bin.v2'
        self.folders.generators = 'bin.v2/generators'

    def source(self):
        git = Git(self)
        data = self.conan_data['sources'][self.version]
        git.fetch_commit(data['url'], data['commit'])
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
        b2.build('boost_msm')

    def package(self):
        b2 = self.python_requires['b2-tools'].module.B2(self)
        b2.build(target='conan-install')

    def package_info(self):
        self.cpp_info.set_property('cmake_target_name', 'Boost::msm')
        self.cpp_info.set_property('b2_target_name', '/boost/msm//boost_msm')

        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.resdirs = ['share']
        self.cpp_info.builddirs = ['share/boost/msm/modules']
    def package_id(self):
        self.info.clear()


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

project /boost/msm ;

alias boost_msm : : : <include>include ;

call-if : boost-library msm ;
'''