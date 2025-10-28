from conan import ConanFile


class BoostParserRecipe(ConanFile):
    name = 'boost-parser'

    license = 'BSL-1.0'
    description = '''A parser combinator library.'''
    author = 'T. Zachary Laine'
    url = 'https://github.com/boostorg/parser.git'
    topics = ['Parsing']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'