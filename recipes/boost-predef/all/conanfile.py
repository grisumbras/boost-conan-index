import os.path
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy
from conan.tools.scm import Git

class BoostPredefRecipe(ConanFile):
    name = 'boost-predef'

    license = 'BSL-1.0'
    description = 'This library defines a set of compiler, architecture, operating system, library, and other version numbers from the information it can gather of C, C++, Objective C, and Objective C++ predefined macros or those defined in generally available headers.'
    author = 'René Ferdinand Rivera Morell'
    url = 'https://github.com/boostorg/predef.git'
    topics = ['Miscellaneous']

    settings = 'compiler'

    package_type = 'header-library'

    def validate(self):
        check_min_cppstd(self, '98')

    

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
        self.cpp_info.set_property('cmake_target_name', 'Boost::Predef')
        self.cpp_info.set_property('b2_project_name', '/boost/predef')