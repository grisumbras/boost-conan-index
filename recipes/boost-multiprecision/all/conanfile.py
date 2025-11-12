from conan import ConanFile


class BoostMultiprecisionRecipe(ConanFile):
    name = 'boost-multiprecision'

    license = 'BSL-1.0'
    description = '''Extended precision arithmetic types for floating point, integer, and rational arithmetic.'''
    author = 'John Maddock, Christopher Kormanyos'
    url = 'https://github.com/boostorg/multiprecision.git'
    topics = ['Math']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'