from conan import ConanFile


class BoostAlgorithmRecipe(ConanFile):
    name = 'boost-algorithm'

    license = 'BSL-1.0'
    description = '''A collection of useful generic algorithms.'''
    author = 'Marshall Clow'
    url = 'https://github.com/boostorg/algorithm.git'
    topics = ['Algorithms']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'