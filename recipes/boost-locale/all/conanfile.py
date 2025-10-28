from conan import ConanFile


class BoostLocaleRecipe(ConanFile):
    name = 'boost-locale'

    license = 'BSL-1.0'
    description = '''Provide localization and Unicode handling tools for C++.'''
    author = 'Artyom Beilis'
    url = 'https://github.com/boostorg/locale.git'
    topics = ['String']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'