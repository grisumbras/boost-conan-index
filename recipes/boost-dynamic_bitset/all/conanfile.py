from conan import ConanFile


class BoostDynamicBitsetRecipe(ConanFile):
    name = 'boost-dynamic_bitset'

    license = 'BSL-1.0'
    description = '''The dynamic_bitset template represents a set of bits. It provides access to the value of individual bits via operator[] and provides all of the bitwise operators that one can apply to builtin integers, such as operator& and operator<<. The number of bits in the set can change at runtime.'''
    author = 'Jeremy Siek, Chuck Allison'
    url = 'https://github.com/boostorg/dynamic_bitset.git'
    topics = ['Data structures']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'