from conan import ConanFile


class BoostSpiritRecipe(ConanFile):
    name = 'boost-spirit'

    license = 'BSL-1.0'
    description = '''LL parser framework represents parsers directly as EBNF grammars in inlined C++.'''
    author = 'Joel de Guzman, Hartmut Kaiser, Dan Nuffer'
    url = 'https://github.com/boostorg/spirit.git'
    topics = ['Parsing', 'String']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'