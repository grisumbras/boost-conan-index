from conan import ConanFile


class BoostIoRecipe(ConanFile):
    name = 'boost-io'

    license = 'BSL-1.0'
    description = '''Utilities for the standard I/O library.'''
    author = 'Daryle Walker, Beman Dawes, Glen Fernandes'
    url = 'https://github.com/boostorg/io.git'
    topics = ['IO']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'