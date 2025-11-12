from conan import ConanFile


class BoostHofRecipe(ConanFile):
    name = 'boost-hof'

    license = 'BSL-1.0'
    description = '''Higher-order functions for C++'''
    author = 'Paul Fultz II'
    url = 'https://github.com/boostorg/hof.git'
    topics = ['Metaprogramming', 'Function-objects']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'