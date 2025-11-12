from conan import ConanFile


class BoostUblasRecipe(ConanFile):
    name = 'boost-ublas'

    license = 'BSL-1.0'
    description = '''uBLAS provides tensor, matrix, and vector classes as well as basic linear algebra routines. Several dense, packed and sparse storage schemes are supported.'''
    author = 'Joerg Walter, Mathias Koch'
    url = 'https://github.com/boostorg/ublas.git'
    topics = ['Math']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'