from conan import ConanFile


class BoostFormatRecipe(ConanFile):
    name = 'boost-format'

    license = 'BSL-1.0'
    description = '''The format library provides a type-safe mechanism for formatting arguments according to a printf-like format-string.'''
    author = 'Samuel Krempp'
    url = 'https://github.com/boostorg/format.git'
    topics = ['IO', 'String']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'