import os.path
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import (
    copy,
    rmdir,
)
from conan.tools.scm import Git

class BoostType_ErasureRecipe(ConanFile):
    name = 'boost-type-erasure'

    license = 'BSL-1.0'
    description = 'Runtime polymorphism based on concepts.'
    author = 'Steven Watanabe'
    url = 'https://github.com/boostorg/type_erasure.git'
    topics = ['Data']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}

    package_type = 'library'

    def validate(self):
        check_min_cppstd(self, '03')

    def build_requirements(self):
       self.tool_requires('b2/[>=5.3.0]')

    def requirements(self):
        for dep in self.conan_data['sources'][self.version]['dependencies']:
            self.requires(
                dep,
                headers=True,
                transitive_headers=True,
                libs=True,
                transitive_libs=True,
            )

    def source(self):
        git = Git(self)
        data = self.conan_data['sources'][self.version]
        git.fetch_commit(data['url'], data['commit'])
        rmdir(self, '.git')

    

    def package_info(self):
        
        self.cpp_info.set_property('cmake_target_name', 'Boost::Type_Erasure')
        self.cpp_info.set_property('b2_project_name', '/boost/type-erasure')