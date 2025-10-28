from conan import ConanFile


class BoostXpressiveRecipe(ConanFile):
    name = 'boost-xpressive'

    license = 'BSL-1.0'
    description = '''Regular expressions that can be written as strings or as expression templates, and which can refer to each other and themselves recursively with the power of context-free grammars.'''
    author = 'Eric Niebler'
    url = 'https://github.com/boostorg/xpressive.git'
    topics = ['String']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'