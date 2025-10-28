from conan import ConanFile


class BoostIntervalRecipe(ConanFile):
    name = 'boost-interval'

    license = 'BSL-1.0'
    description = '''Extends the usual arithmetic functions to mathematical intervals.'''
    author = 'Guillaume Melquiond, Hervé Brönnimann, Sylvain Pion'
    url = 'https://github.com/boostorg/interval.git'
    topics = ['Math']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'