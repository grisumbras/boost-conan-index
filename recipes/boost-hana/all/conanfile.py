from conan import ConanFile


class BoostHanaRecipe(ConanFile):
    name = 'boost-hana'

    license = 'BSL-1.0'
    description = '''A modern C++ metaprogramming library. It provides high level algorithms to manipulate heterogeneous sequences, allows writing type-level computations with a natural syntax, provides tools to introspect user-defined types and much more.'''
    author = 'Louis Dionne'
    url = 'https://github.com/boostorg/hana.git'
    topics = ['Metaprogramming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'