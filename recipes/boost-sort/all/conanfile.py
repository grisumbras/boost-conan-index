from conan import ConanFile


class BoostSortRecipe(ConanFile):
    name = 'boost-sort'

    license = 'BSL-1.0'
    description = '''High-performance templated sort functions.'''
    author = 'Steven Ross'
    url = 'https://github.com/boostorg/sort.git'
    topics = ['Algorithms']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'