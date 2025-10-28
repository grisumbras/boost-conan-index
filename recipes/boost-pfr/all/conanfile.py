from conan import ConanFile


class BoostPfrRecipe(ConanFile):
    name = 'boost-pfr'

    license = 'BSL-1.0'
    description = '''Basic reflection  for user defined types.'''
    author = 'Antony Polukhin'
    url = 'https://github.com/boostorg/pfr.git'
    topics = ['Data', 'Metaprogramming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'