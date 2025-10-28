from conan import ConanFile


class BoostInterprocessRecipe(ConanFile):
    name = 'boost-interprocess'

    license = 'BSL-1.0'
    description = '''Shared memory, memory mapped files, process-shared mutexes, condition variables, containers and allocators.'''
    author = 'Ion Gaztañaga'
    url = 'https://github.com/boostorg/interprocess.git'
    topics = ['Concurrent']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'