from conan import ConanFile


class BoostPropertyMapParallelRecipe(ConanFile):
    name = 'boost-property_map_parallel'

    license = 'BSL-1.0'
    description = '''Parallel extensions to Property Map for use with Parallel Graph.'''
    author = 'Jeremy Siek'
    url = 'https://github.com/boostorg/property_map_parallel.git'
    topics = ['Containers', 'Generic']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'