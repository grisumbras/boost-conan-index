from conan import ConanFile


class BoostGraphParallelRecipe(ConanFile):
    name = 'boost-graph_parallel'

    license = 'BSL-1.0'
    description = '''The PBGL graph interface and graph components are generic, in the same sense as the Standard Template Library (STL).'''
    author = 'Jeremy Siek, Doug Gregor, and a University of Notre Dame team.'
    url = 'https://github.com/boostorg/graph_parallel.git'
    topics = ['Algorithms', 'Containers', 'Iterators']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'