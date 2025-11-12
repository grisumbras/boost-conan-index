from conan import ConanFile


class BoostBimapRecipe(ConanFile):
    name = 'boost-bimap'

    license = 'BSL-1.0'
    description = '''Bidirectional maps library for C++. With Boost.Bimap you can create associative containers in which both types can be used as key.'''
    author = 'Matias Capeletto'
    url = 'https://github.com/boostorg/bimap.git'
    topics = ['Containers', 'Data']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'