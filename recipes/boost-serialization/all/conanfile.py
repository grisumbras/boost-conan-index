from conan import ConanFile


class BoostSerializationRecipe(ConanFile):
    name = 'boost-serialization'

    license = 'BSL-1.0'
    description = '''Serialization for persistence and marshalling.'''
    author = 'Robert Ramey'
    url = 'https://github.com/boostorg/serialization.git'
    topics = ['IO']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'