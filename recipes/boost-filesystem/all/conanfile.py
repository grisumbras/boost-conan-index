import os.path
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import (
    copy,
    rmdir,
)
from conan.tools.scm import Git

class BoostFilesystemRecipe(ConanFile):
    name = 'boost-filesystem'

    license = 'BSL-1.0'
    description = '''The Boost Filesystem Library provides portable facilities to query and manipulate paths, files, and directories.'''
    author = 'Beman Dawes'
    url = 'https://github.com/boostorg/filesystem.git'
    topics = ['System']

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
        rmdir(self, '.git')

    

    def package_info(self):
        
        self.cpp_info.resdirs = ['share']
        self.cpp_info.set_property('cmake_target_name', 'Boost::Filesystem')
        self.cpp_info.set_property('b2_project_name', '/boost/filesystem')