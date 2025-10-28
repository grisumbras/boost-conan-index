from conan import ConanFile


class BoostFunctionRecipe(ConanFile):
    name = 'boost-function'

    license = 'BSL-1.0'
    description = '''Function object wrappers for deferred calls or callbacks.'''
    author = 'Doug Gregor'
    url = 'https://github.com/boostorg/function.git'
    topics = ['Function-objects', 'Programming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'