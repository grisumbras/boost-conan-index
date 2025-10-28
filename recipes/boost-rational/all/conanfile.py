from conan import ConanFile


class BoostRationalRecipe(ConanFile):
    name = 'boost-rational'

    license = 'BSL-1.0'
    description = '''A rational number class.'''
    author = 'Paul Moore'
    url = 'https://github.com/boostorg/rational.git'
    topics = ['Math']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'