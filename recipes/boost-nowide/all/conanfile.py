from conan import ConanFile


class BoostNowideRecipe(ConanFile):
    name = 'boost-nowide'

    license = 'BSL-1.0'
    description = '''Standard library functions with UTF-8 API on Windows.'''
    author = 'Artyom Beilis'
    url = 'https://github.com/boostorg/nowide.git'
    topics = ['System']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'