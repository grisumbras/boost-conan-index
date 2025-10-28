from conan import ConanFile


class BoostIntegerRecipe(ConanFile):
    name = 'boost-integer'

    license = 'BSL-1.0'
    description = '''The organization of boost integer headers and classes is designed to take advantage of <stdint.h> types from the 1999 C standard without resorting to undefined behavior in terms of the 1998 C++ standard. The header <boost/cstdint.hpp> makes the standard integer types safely available in namespace boost without placing any names in namespace std.'''
    author = ''
    url = 'https://github.com/boostorg/integer.git'
    topics = ['Math']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'