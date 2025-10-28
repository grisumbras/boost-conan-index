from conan import ConanFile


class BoostSignals2Recipe(ConanFile):
    name = 'boost-signals2'

    license = 'BSL-1.0'
    description = '''Managed signals & slots callback implementation (thread-safe version 2).'''
    author = 'Frank Mori Hess'
    url = 'https://github.com/boostorg/signals2.git'
    topics = ['Function-objects', 'Patterns']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'