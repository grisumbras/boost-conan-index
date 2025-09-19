import os.path
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import (
    copy,
    rmdir,
)
from conan.tools.scm import Git

class BoostGeometryRecipe(ConanFile):
    name = 'boost-geometry'

    license = 'BSL-1.0'
    description = 'The Boost.Geometry library provides geometric algorithms, primitives and spatial index.'
    author = 'Barend Gehrels, Bruno Lalande, Mateusz Loskot, Adam Wulkiewicz, Menelaos Karavelas, Vissarion Fisikopoulos'
    url = 'https://github.com/boostorg/geometry.git'
    topics = ['Algorithms', 'Data', 'Math']

    settings = 'compiler'
    no_copy_source = True

    package_type = 'header-library'

    def validate(self):
        check_min_cppstd(self, '14')

    

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
        rmdir(self, '.git')

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
        self.cpp_info.set_property('cmake_target_name', 'Boost::Geometry')
        self.cpp_info.set_property('b2_project_name', '/boost/geometry')