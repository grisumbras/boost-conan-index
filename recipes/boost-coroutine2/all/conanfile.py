from conan import ConanFile


class BoostCoroutine2Recipe(ConanFile):
    name = 'boost-coroutine2'

    license = 'BSL-1.0'
    description = '''(C++11) Coroutine library.'''
    author = 'Oliver Kowalke'
    url = 'https://github.com/boostorg/coroutine2.git'
    topics = ['Concurrent']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'