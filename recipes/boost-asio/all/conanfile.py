from conan import ConanFile


class BoostAsioRecipe(ConanFile):
    name = 'boost-asio'

    license = 'BSL-1.0'
    description = '''Portable networking and other low-level I/O, including sockets, timers, hostname resolution, socket iostreams, serial ports, file descriptors and Windows HANDLEs.'''
    author = 'Chris Kohlhoff'
    url = 'https://github.com/boostorg/asio.git'
    topics = ['Concurrent', 'IO']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'