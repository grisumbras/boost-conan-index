import os.path
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy
from conan.tools.scm import Git

class BoostFiberRecipe(ConanFile):
    name = 'boost-fiber'

    license = 'BSL-1.0'
    description = '(C++11) Userland threads library.'
    author = 'Oliver Kowalke'
    url = 'https://github.com/boostorg/fiber.git'
    topics = ['Concurrent', 'System']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}

    package_type = 'library'

    def validate(self):
        check_min_cppstd(self, '11')

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

    

    def package_info(self):
        
        self.cpp_info.set_property('cmake_target_name', 'Boost::Fiber')
        self.cpp_info.set_property('b2_project_name', '/boost/fiber')