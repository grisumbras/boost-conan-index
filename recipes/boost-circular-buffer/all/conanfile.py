import os.path
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy
from conan.tools.scm import Git

class BoostCircular_BufferRecipe(ConanFile):
    name = 'boost-circular-buffer'

    license = 'BSL-1.0'
    description = 'A STL compliant container also known as ring or cyclic buffer.'
    author = 'Jan Gaspar'
    url = 'https://github.com/boostorg/circular_buffer.git'
    topics = ['Containers']

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
        self.cpp_info.set_property('cmake_target_name', 'Boost::Circular_Buffer')
        self.cpp_info.set_property('b2_project_name', '/boost/circular-buffer')