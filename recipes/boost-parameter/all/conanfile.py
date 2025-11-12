from conan import ConanFile


class BoostParameterRecipe(ConanFile):
    name = 'boost-parameter'

    license = 'BSL-1.0'
    description = '''Boost.Parameter Library - Write functions that accept arguments by name.'''
    author = 'David Abrahams, Daniel Wallin'
    url = 'https://github.com/boostorg/parameter.git'
    topics = ['Emulation', 'Programming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'