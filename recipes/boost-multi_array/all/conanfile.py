from conan import ConanFile


class BoostMultiArrayRecipe(ConanFile):
    name = 'boost-multi_array'

    license = 'BSL-1.0'
    description = '''Boost.MultiArray provides a generic N-dimensional array concept definition and common implementations of that interface.'''
    author = 'Ron Garcia'
    url = 'https://github.com/boostorg/multi_array.git'
    topics = ['Containers', 'Math']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'