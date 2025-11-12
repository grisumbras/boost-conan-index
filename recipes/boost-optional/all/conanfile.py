from conan import ConanFile


class BoostOptionalRecipe(ConanFile):
    name = 'boost-optional'

    license = 'BSL-1.0'
    description = '''A value-semantic, type-safe wrapper for representing 'optional' (or 'nullable') objects of a given type. An optional object may or may not contain a value of the underlying type.'''
    author = 'Fernando Cacciola'
    url = 'https://github.com/boostorg/optional.git'
    topics = ['Data']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'