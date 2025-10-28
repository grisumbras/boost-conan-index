from conan import ConanFile


class BoostCrcRecipe(ConanFile):
    name = 'boost-crc'

    license = 'BSL-1.0'
    description = '''The Boost CRC Library provides two implementations of CRC (cyclic redundancy code) computation objects and two implementations of CRC computation functions. The implementations are template-based.'''
    author = 'Daryle Walker'
    url = 'https://github.com/boostorg/crc.git'
    topics = ['Domain']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'