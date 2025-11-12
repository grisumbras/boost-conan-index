from conan import ConanFile


class BoostAlignRecipe(ConanFile):
    name = 'boost-align'

    license = 'BSL-1.0'
    description = '''Memory alignment functions, allocators, traits.'''
    author = 'Glen Fernandes'
    url = 'https://github.com/boostorg/align.git'
    topics = ['Memory']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'