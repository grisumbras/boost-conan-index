from conan import ConanFile


class BoostUnorderedRecipe(ConanFile):
    name = 'boost-unordered'

    license = 'BSL-1.0'
    description = '''Unordered associative containers.'''
    author = 'Daniel James'
    url = 'https://github.com/boostorg/unordered.git'
    topics = ['Containers']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'