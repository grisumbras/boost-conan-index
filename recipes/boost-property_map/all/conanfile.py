from conan import ConanFile


class BoostPropertyMapRecipe(ConanFile):
    name = 'boost-property_map'

    license = 'BSL-1.0'
    description = '''Concepts defining interfaces which map key objects to value objects.'''
    author = 'Jeremy Siek'
    url = 'https://github.com/boostorg/property_map.git'
    topics = ['Containers', 'Generic']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'