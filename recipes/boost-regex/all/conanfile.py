from conan import ConanFile


class BoostRegexRecipe(ConanFile):
    name = 'boost-regex'

    license = 'BSL-1.0'
    description = '''Regular expression library.'''
    author = 'John Maddock'
    url = 'https://github.com/boostorg/regex.git'
    topics = ['String']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'