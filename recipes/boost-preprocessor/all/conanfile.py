from conan import ConanFile


class BoostPreprocessorRecipe(ConanFile):
    name = 'boost-preprocessor'

    license = 'BSL-1.0'
    description = '''Preprocessor metaprogramming tools including repetition and recursion.'''
    author = 'Vesa Karvonen, Paul Mensonides'
    url = 'https://github.com/boostorg/preprocessor.git'
    topics = ['Preprocessor']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'