from conan import ConanFile


class BoostScopeExitRecipe(ConanFile):
    name = 'boost-scope_exit'

    license = 'BSL-1.0'
    description = '''Execute arbitrary code at scope exit.'''
    author = 'Alexander Nasonov'
    url = 'https://github.com/boostorg/scope_exit.git'
    topics = ['Emulation']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'