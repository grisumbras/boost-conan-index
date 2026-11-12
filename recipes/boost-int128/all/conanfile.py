from conan import ConanFile


class BoostInt128Recipe(ConanFile):
    name = 'boost-int128'

    license = 'BSL-1.0'
    description = '''Portable and Performant 128-bit Integers'''
    author = 'Matt Borland'
    url = 'https://github.com/boostorg/int128.git'
    topics = ['Math']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'