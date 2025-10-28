from conan import ConanFile


class BoostMpiRecipe(ConanFile):
    name = 'boost-mpi'

    license = 'BSL-1.0'
    description = '''Message Passing Interface library, for use in distributed-memory parallel application programming.'''
    author = 'Douglas Gregor, Matthias Troyer'
    url = 'https://github.com/boostorg/mpi.git'
    topics = ['Concurrent']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'