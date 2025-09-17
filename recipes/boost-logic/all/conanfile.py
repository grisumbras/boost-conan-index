import os.path
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy
from conan.tools.scm import Git

class BoostLogicRecipe(ConanFile):
    name = 'boost-logic'

    license = 'BSL-1.0'
    description = '3-state boolean type library.'
    author = 'Doug Gregor'
    url = 'https://github.com/boostorg/logic.git'
    topics = ['Miscellaneous']

    settings = 'compiler'

    package_type = 'header-library'

    def validate(self):
        check_min_cppstd(self, '03')

    

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
        self.cpp_info.set_property('cmake_target_name', 'Boost::Logic')
        self.cpp_info.set_property('b2_project_name', '/boost/logic')