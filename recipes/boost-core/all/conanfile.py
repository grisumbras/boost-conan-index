from conan import ConanFile


class BoostCoreRecipe(ConanFile):
    name = 'boost-core'

    license = 'BSL-1.0'
    description = '''A collection of simple core utilities with minimal dependencies.'''
    author = 'Peter Dimov, Glen Fernandes, Andrey Semashev'
    url = 'https://github.com/boostorg/core.git'
    topics = ['Miscellaneous']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'