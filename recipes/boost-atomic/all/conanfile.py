from conan import ConanFile


class BoostAtomicRecipe(ConanFile):
    name = 'boost-atomic'

    license = 'BSL-1.0'
    description = '''C++11-style atomic types.'''
    author = 'Helge Bahmann, Tim Blechmann, Andrey Semashev'
    url = 'https://github.com/boostorg/atomic.git'
    topics = ['Concurrent']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'