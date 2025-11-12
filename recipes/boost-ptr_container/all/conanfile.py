from conan import ConanFile


class BoostPtrContainerRecipe(ConanFile):
    name = 'boost-ptr_container'

    license = 'BSL-1.0'
    description = '''Containers for storing heap-allocated polymorphic objects to ease OO-programming.'''
    author = 'Thorsten Ottosen'
    url = 'https://github.com/boostorg/ptr_container.git'
    topics = ['Containers', 'Data']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'