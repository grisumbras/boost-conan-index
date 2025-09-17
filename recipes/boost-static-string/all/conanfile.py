import os.path
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy
from conan.tools.scm import Git

class BoostStatic_StringRecipe(ConanFile):
    name = 'boost-static-string'

    license = 'BSL-1.0'
    description = 'A fixed capacity dynamically sized string.'
    author = 'Krystian Stasiowski, Vinnie Falco'
    url = 'https://github.com/boostorg/static_string.git'
    topics = ['Container', 'String']

    settings = 'compiler'

    package_type = 'header-library'

    def validate(self):
        check_min_cppstd(self, '11')

    

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
        self.cpp_info.set_property('cmake_target_name', 'Boost::Static_String')
        self.cpp_info.set_property('b2_project_name', '/boost/static-string')