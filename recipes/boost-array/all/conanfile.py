from conan import ConanFile


class BoostArrayRecipe(ConanFile):
    name = 'boost-array'

    license = 'BSL-1.0'
    description = '''STL compliant container wrapper for arrays of constant size.'''
    author = 'Nicolai Josuttis'
    url = 'https://github.com/boostorg/array.git'
    topics = ['Containers']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'