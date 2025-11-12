from conan import ConanFile


class BoostLogRecipe(ConanFile):
    name = 'boost-log'

    license = 'BSL-1.0'
    description = '''Logging library.'''
    author = 'Andrey Semashev'
    url = 'https://github.com/boostorg/log.git'
    topics = ['Miscellaneous']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'