from conan import ConanFile


class BoostThrowExceptionRecipe(ConanFile):
    name = 'boost-throw_exception'

    license = 'BSL-1.0'
    description = '''A common infrastructure for throwing exceptions from Boost libraries.'''
    author = 'Emil Dotchevski, Peter Dimov'
    url = 'https://github.com/boostorg/throw_exception.git'
    topics = ['Emulation', 'Error-handling']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'