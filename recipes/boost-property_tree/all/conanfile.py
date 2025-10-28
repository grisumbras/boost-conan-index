from conan import ConanFile


class BoostPropertyTreeRecipe(ConanFile):
    name = 'boost-property_tree'

    license = 'BSL-1.0'
    description = '''A tree data structure especially suited to storing configuration data.'''
    author = 'Marcin Kalicinski, Sebastian Redl'
    url = 'https://github.com/boostorg/property_tree.git'
    topics = ['Containers', 'Data']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'