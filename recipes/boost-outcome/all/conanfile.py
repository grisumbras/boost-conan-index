from conan import ConanFile


class BoostOutcomeRecipe(ConanFile):
    name = 'boost-outcome'

    license = 'BSL-1.0'
    description = '''A deterministic failure handling library partially simulating lightweight exceptions.'''
    author = 'Niall Douglas'
    url = 'https://github.com/boostorg/outcome.git'
    topics = ['Patterns', 'Emulation', 'Programming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'