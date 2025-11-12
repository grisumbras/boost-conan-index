from conan import ConanFile


class BoostPoolRecipe(ConanFile):
    name = 'boost-pool'

    license = 'BSL-1.0'
    description = '''Memory pool management.'''
    author = 'Steve Cleary'
    url = 'https://github.com/boostorg/pool.git'
    topics = ['Memory']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'