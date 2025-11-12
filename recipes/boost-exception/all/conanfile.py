from conan import ConanFile


class BoostExceptionRecipe(ConanFile):
    name = 'boost-exception'

    license = 'BSL-1.0'
    description = '''The Boost Exception library supports transporting of arbitrary data in exception objects, and transporting of exceptions between threads.'''
    author = 'Emil Dotchevski'
    url = 'https://github.com/boostorg/exception.git'
    topics = ['Error-handling', 'Emulation']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'