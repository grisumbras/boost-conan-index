from conan import ConanFile


class BoostHash2Recipe(ConanFile):
    name = 'boost-hash2'

    license = 'BSL-1.0'
    description = '''An extensible hashing framework.'''
    author = 'Peter Dimov, Christian Mazakas'
    url = 'https://github.com/boostorg/hash2.git'
    topics = ['Function-objects']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'