import os.path
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy
from conan.tools.scm import Git

class BoostDetailRecipe(ConanFile):
    name = 'boost-detail'

    license = 'BSL-1.0'
    description = 'This library contains a set of header only utilities used internally by Boost C++ Libraries to facilitate their implementation.'
    author = 'David Abrahams, Beman Dawes, Eric Friedman, Ronald Garcia, Howard Hinnant, Daniel James, Bryce Lelbach, Joaquin M Lopez Munoz, Jeremy Siek, Matthias Troyerk'
    url = 'https://github.com/boostorg/detail.git'
    topics = ['Miscellaneous']

    

    package_type = 'header-library'

    

    

    def requirements(self):
        for dep in self.conan_data['sources'][self.version]['dependencies']:
            self.requires(
                dep,
                headers=True,
                transitive_headers=True,)

    def source(self):
        git = Git(self)
        data = self.conan_data['sources'][self.version]
        git.fetch_commit(data['url'], data['commit'])

    def build(self):
        pass

    def package(self):
        copy(self, '*',
            os.path.join(self.source_folder, 'include'),
            os.path.join(self.package_folder, 'include'))

    def package_id(self):
        self.info.clear()

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.set_property('cmake_target_name', 'Boost::Detail')
        self.cpp_info.set_property('b2_project_name', '/boost/detail')
