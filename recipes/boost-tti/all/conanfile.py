from conan import ConanFile


class BoostTtiRecipe(ConanFile):
    name = 'boost-tti'

    license = 'BSL-1.0'
    description = '''Type Traits Introspection library.'''
    author = 'Edward Diener'
    url = 'https://github.com/boostorg/tti.git'
    topics = ['Generic', 'Metaprogramming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'