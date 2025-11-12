from conan import ConanFile


class BoostBloomRecipe(ConanFile):
    name = 'boost-bloom'

    license = 'BSL-1.0'
    description = '''Bloom filters.'''
    author = 'Joaquín M López Muñoz'
    url = 'https://github.com/boostorg/bloom.git'
    topics = ['Containers']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'