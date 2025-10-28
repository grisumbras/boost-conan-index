from conan import ConanFile


class BoostRandomRecipe(ConanFile):
    name = 'boost-random'

    license = 'BSL-1.0'
    description = '''A complete system for random number generation.'''
    author = 'Jens Maurer'
    url = 'https://github.com/boostorg/random.git'
    topics = ['Math']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'