from conan import ConanFile


class BoostDecimalRecipe(ConanFile):
    name = 'boost-decimal'

    license = 'BSL-1.0'
    description = '''An implementation of IEEE754 Decimal Floating Point Numbers.'''
    author = 'Matt Borland, Christopher Kormanyos'
    url = 'https://github.com/boostorg/decimal.git'
    topics = ['Math and numerics']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'