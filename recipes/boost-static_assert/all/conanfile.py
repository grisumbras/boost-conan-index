from conan import ConanFile


class BoostStaticAssertRecipe(ConanFile):
    name = 'boost-static_assert'

    license = 'BSL-1.0'
    description = '''Static assertions (compile time assertions).'''
    author = 'John Maddock'
    url = 'https://github.com/boostorg/static_assert.git'
    topics = ['Correctness', 'Generic', 'Metaprogramming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'