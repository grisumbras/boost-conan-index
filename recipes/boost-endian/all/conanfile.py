from conan import ConanFile


class BoostEndianRecipe(ConanFile):
    name = 'boost-endian'

    license = 'BSL-1.0'
    description = '''Types and conversion functions for correct byte ordering and more regardless of processor endianness.'''
    author = 'Beman Dawes'
    url = 'https://github.com/boostorg/endian.git'
    topics = ['IO', 'Math', 'Miscellaneous']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'