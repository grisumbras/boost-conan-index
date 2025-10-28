from conan import ConanFile


class BoostBeastRecipe(ConanFile):
    name = 'boost-beast'

    license = 'BSL-1.0'
    description = '''Portable HTTP, WebSocket, and network operations using only C++11 and Boost.Asio'''
    author = 'Vinnie Falco'
    url = 'https://github.com/boostorg/beast.git'
    topics = ['Concurrent', 'IO']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'