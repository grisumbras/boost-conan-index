from conan import ConanFile


class BoostSystemRecipe(ConanFile):
    name = 'boost-system'

    license = 'BSL-1.0'
    description = '''Extensible error reporting.'''
    author = 'Beman Dawes'
    url = 'https://github.com/boostorg/system.git'
    topics = ['System', 'Error-handling', 'Programming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'