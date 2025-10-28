from conan import ConanFile


class BoostAccumulatorsRecipe(ConanFile):
    name = 'boost-accumulators'

    license = 'BSL-1.0'
    description = '''Framework for incremental calculation, and collection of statistical accumulators.'''
    author = 'Eric Niebler'
    url = 'https://github.com/boostorg/accumulators.git'
    topics = ['Math']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'