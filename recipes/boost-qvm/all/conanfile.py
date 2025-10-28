from conan import ConanFile


class BoostQvmRecipe(ConanFile):
    name = 'boost-qvm'

    license = 'BSL-1.0'
    description = '''Generic C++ library for working with Quaternions Vectors and Matrices.'''
    author = 'Emil Dotchevski'
    url = 'https://github.com/boostorg/qvm.git'
    topics = ['Generic', 'Math', 'Algorithms']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'