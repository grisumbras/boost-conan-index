from conan import ConanFile


class BoostGraphRecipe(ConanFile):
    name = 'boost-graph'

    license = 'BSL-1.0'
    description = '''The BGL graph interface and graph components are generic, in the same sense as the Standard Template Library (STL).'''
    author = 'Jeremy Siek and a University of Notre Dame team.'
    url = 'https://github.com/boostorg/graph.git'
    topics = ['Algorithms', 'Containers', 'Iterators']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'