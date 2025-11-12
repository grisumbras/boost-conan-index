from conan import ConanFile


class BoostDetailRecipe(ConanFile):
    name = 'boost-detail'

    license = 'BSL-1.0'
    description = '''This library contains a set of header only utilities used internally by Boost C++ Libraries to facilitate their implementation.'''
    author = 'David Abrahams, Beman Dawes, Eric Friedman, Ronald Garcia, Howard Hinnant, Daniel James, Bryce Lelbach, Joaquin M Lopez Munoz, Jeremy Siek, Matthias Troyerk'
    url = 'https://github.com/boostorg/detail.git'
    topics = ['Miscellaneous']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'