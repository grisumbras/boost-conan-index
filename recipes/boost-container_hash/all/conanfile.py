from conan import ConanFile


class BoostContainerHashRecipe(ConanFile):
    name = 'boost-container_hash'

    license = 'BSL-1.0'
    description = '''An STL-compatible hash function object that can be extended to hash user defined types.'''
    author = 'Daniel James'
    url = 'https://github.com/boostorg/container_hash.git'
    topics = ['Function-objects']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'