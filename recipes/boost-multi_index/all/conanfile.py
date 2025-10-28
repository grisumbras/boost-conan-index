from conan import ConanFile


class BoostMultiIndexRecipe(ConanFile):
    name = 'boost-multi_index'

    license = 'BSL-1.0'
    description = '''The Boost Multi-index Containers Library provides a class template named multi_index_container which enables the construction of containers maintaining one or more indices with different sorting and access semantics.'''
    author = 'Joaquín M López Muñoz'
    url = 'https://github.com/boostorg/multi_index.git'
    topics = ['Containers', 'Data']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'