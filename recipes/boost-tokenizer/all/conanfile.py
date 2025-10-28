from conan import ConanFile


class BoostTokenizerRecipe(ConanFile):
    name = 'boost-tokenizer'

    license = 'BSL-1.0'
    description = '''Break of a string or other character sequence into a series of tokens.'''
    author = 'John Bandela'
    url = 'https://github.com/boostorg/tokenizer.git'
    topics = ['Iterators', 'String']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'