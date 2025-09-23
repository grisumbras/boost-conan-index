import os.path
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import (
    copy,
    rmdir,
)
from conan.tools.scm import Git

class BoostMulti_IndexRecipe(ConanFile):
    name = 'boost-multi-index'

    license = 'BSL-1.0'
    description = 'The Boost Multi-index Containers Library provides a class template named multi_index_container which enables the construction of containers maintaining one or more indices with different sorting and access semantics.'
    author = 'Joaquín M López Muñoz'
    url = 'https://github.com/boostorg/multi_index.git'
    topics = ['Containers', 'Data']

    settings = 'compiler'
    no_copy_source = True

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
        rmdir(self, '.git')

    def build(self):
        pass

    def package(self):
        copy(
            self,
            '*',
            os.path.join(self.source_folder, 'include'),
            os.path.join(self.package_folder, 'include'),
        )
        copy(
            self,
            'LICENSE*',
            self.source_folder,
            os.path.join(
                self.package_folder, 'share', 'boost', 'multi_index',
            ),
        )

    def package_id(self):
        self.info.clear()

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.resdirs = ['share']
        self.cpp_info.set_property('cmake_target_name', 'Boost::Multi_Index')
        self.cpp_info.set_property('b2_project_name', '/boost/multi-index')