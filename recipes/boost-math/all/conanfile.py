from conan import ConanFile


class BoostMathRecipe(ConanFile):
    name = 'boost-math'

    license = 'BSL-1.0'
    description = '''Boost.Math includes several contributions in the domain of mathematics: Floating Point Utilities, Specific Width Floating Point Types, Mathematical Constants, Statistical Distributions, Special Functions, Root Finding and Function Minimization, Polynomials and Rational Functions, Interpolation, and Numerical Integration and Differentiation. Many of these features are templated to support both built-in, and extended width types (e.g. Boost.Multiprecision)'''
    author = 'various'
    url = 'https://github.com/boostorg/math.git'
    topics = ['Math']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'