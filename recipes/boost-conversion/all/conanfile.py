from conan import ConanFile


class BoostConversionRecipe(ConanFile):
    name = 'boost-conversion'

    license = 'BSL-1.0'
    description = '''Polymorphic casts.'''
    author = 'Dave Abrahams, Kevlin Henney'
    url = 'https://github.com/boostorg/conversion.git'
    topics = ['Miscellaneous']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'