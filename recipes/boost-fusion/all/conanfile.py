from conan import ConanFile


class BoostFusionRecipe(ConanFile):
    name = 'boost-fusion'

    license = 'BSL-1.0'
    description = '''Library for working with tuples, including various containers, algorithms, etc.'''
    author = 'Joel de Guzman, Dan Marsden, Tobias Schwinger'
    url = 'https://github.com/boostorg/fusion.git'
    topics = ['Data', 'Metaprogramming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'