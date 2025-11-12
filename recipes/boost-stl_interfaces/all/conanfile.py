from conan import ConanFile


class BoostStlInterfacesRecipe(ConanFile):
    name = 'boost-stl_interfaces'

    license = 'BSL-1.0'
    description = '''C++14 and later CRTP templates for defining iterators, views, and containers.'''
    author = 'T. Zachary Laine'
    url = 'https://github.com/boostorg/stl_interfaces.git'
    topics = ['Generic']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'