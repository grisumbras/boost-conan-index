from conan import ConanFile


class BoostNumericConversionRecipe(ConanFile):
    name = 'boost-numeric_conversion'

    license = 'BSL-1.0'
    description = '''Optimized Policy-based Numeric Conversions.'''
    author = 'Fernando Cacciola'
    url = 'https://github.com/boostorg/numeric_conversion.git'
    topics = ['Math', 'Miscellaneous']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'