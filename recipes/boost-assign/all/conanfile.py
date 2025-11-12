from conan import ConanFile


class BoostAssignRecipe(ConanFile):
    name = 'boost-assign'

    license = 'BSL-1.0'
    description = '''Filling containers with constant or generated data has never been easier.'''
    author = 'Thorsten Ottosen'
    url = 'https://github.com/boostorg/assign.git'
    topics = ['IO']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'