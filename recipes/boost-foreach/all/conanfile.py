import os.path
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy
from conan.tools.scm import Git

class BoostForeachRecipe(ConanFile):
    name = 'boost-foreach'

    license = 'BSL-1.0'
    description = 'In C++, writing a loop that iterates over a sequence is tedious. We can either use iterators, which requires a considerable amount of boiler-plate, or we can use the std::for_each() algorithm and move our loop body into a predicate, which requires no less boiler-plate and forces us to move our logic far from where it will be used. In contrast, some other languages, like Perl, provide a dedicated "foreach" construct that automates this process. BOOST_FOREACH is just such a construct for C++. It iterates over sequences for us, freeing us from having to deal directly with iterators or write predicates.'
    author = 'Eric Niebler'
    url = 'https://github.com/boostorg/foreach.git'
    topics = ['Algorithms', 'Emulation']

    

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
        self.cpp_info.set_property('cmake_target_name', 'Boost::Foreach')
        self.cpp_info.set_property('b2_project_name', '/boost/foreach')