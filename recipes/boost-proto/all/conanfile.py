from conan import ConanFile


class BoostProtoRecipe(ConanFile):
    name = 'boost-proto'

    license = 'BSL-1.0'
    description = '''Expression template library and compiler construction toolkit for domain-specific embedded languages.'''
    author = 'Eric Niebler'
    url = 'https://github.com/boostorg/proto.git'
    topics = ['Metaprogramming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'