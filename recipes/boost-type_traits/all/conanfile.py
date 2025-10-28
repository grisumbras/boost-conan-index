from conan import ConanFile


class BoostTypeTraitsRecipe(ConanFile):
    name = 'boost-type_traits'

    license = 'BSL-1.0'
    description = '''Templates for fundamental properties of types.'''
    author = 'John Maddock, Steve Cleary, et al'
    url = 'https://github.com/boostorg/type_traits.git'
    topics = ['Generic', 'Metaprogramming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'