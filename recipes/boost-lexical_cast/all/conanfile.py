from conan import ConanFile


class BoostLexicalCastRecipe(ConanFile):
    name = 'boost-lexical_cast'

    license = 'BSL-1.0'
    description = '''General literal text conversions, such as an int represented a string, or vice-versa.'''
    author = 'Kevlin Henney'
    url = 'https://github.com/boostorg/lexical_cast.git'
    topics = ['Miscellaneous', 'String']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'