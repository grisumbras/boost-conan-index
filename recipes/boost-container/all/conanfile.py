from conan import ConanFile


class BoostContainerRecipe(ConanFile):
    name = 'boost-container'

    license = 'BSL-1.0'
    description = '''Standard library containers and extensions.'''
    author = 'Ion Gaztañaga'
    url = 'https://github.com/boostorg/container.git'
    topics = ['Containers', 'Data']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'