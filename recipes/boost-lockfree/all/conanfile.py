from conan import ConanFile


class BoostLockfreeRecipe(ConanFile):
    name = 'boost-lockfree'

    license = 'BSL-1.0'
    description = '''Lockfree data structures.'''
    author = 'Tim Blechmann'
    url = 'https://github.com/boostorg/lockfree.git'
    topics = ['Concurrent']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'