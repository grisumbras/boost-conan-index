from conan import ConanFile


class BoostRangeRecipe(ConanFile):
    name = 'boost-range'

    license = 'BSL-1.0'
    description = '''A new infrastructure for generic algorithms that builds on top of the new iterator concepts.'''
    author = 'Niel Groves, Thorsten Ottosen'
    url = 'https://github.com/boostorg/range.git'
    topics = ['Algorithms']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'