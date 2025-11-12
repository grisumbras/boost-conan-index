from conan import ConanFile


class BoostVmdRecipe(ConanFile):
    name = 'boost-vmd'

    license = 'BSL-1.0'
    description = '''Variadic Macro Data library.'''
    author = 'Edward Diener'
    url = 'https://github.com/boostorg/vmd.git'
    topics = ['Preprocessor']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'