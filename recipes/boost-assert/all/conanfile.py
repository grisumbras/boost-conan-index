from conan import ConanFile


class BoostAssertRecipe(ConanFile):
    name = 'boost-assert'

    license = 'BSL-1.0'
    description = '''Customizable assert macros.'''
    author = 'Peter Dimov'
    url = 'https://github.com/boostorg/assert.git'
    topics = ['Correctness', 'Error-handling']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'