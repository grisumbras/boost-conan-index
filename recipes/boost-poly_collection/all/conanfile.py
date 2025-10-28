from conan import ConanFile


class BoostPolyCollectionRecipe(ConanFile):
    name = 'boost-poly_collection'

    license = 'BSL-1.0'
    description = '''Fast containers of polymorphic objects.'''
    author = 'Joaquín M López Muñoz'
    url = 'https://github.com/boostorg/poly_collection.git'
    topics = ['Containers']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'