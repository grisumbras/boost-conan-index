from conan import ConanFile


class BoostCobaltRecipe(ConanFile):
    name = 'boost-cobalt'

    license = 'BSL-1.0'
    description = '''Coroutines. Basic Algorithms & Types'''
    author = 'Klemens Morgenstern'
    url = 'https://github.com/boostorg/cobalt.git'
    topics = ['Concurrent', 'Coroutines', 'Awaitables', 'Asynchronous']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'