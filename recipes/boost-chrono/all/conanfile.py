from conan import ConanFile


class BoostChronoRecipe(ConanFile):
    name = 'boost-chrono'

    license = 'BSL-1.0'
    description = '''Useful time utilities. C++11.'''
    author = 'Howard Hinnant, Beman Dawes, Vicente J. Botet Escriba'
    url = 'https://github.com/boostorg/chrono.git'
    topics = ['Domain', 'System']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'