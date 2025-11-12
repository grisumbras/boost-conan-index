from conan import ConanFile


class BoostFlyweightRecipe(ConanFile):
    name = 'boost-flyweight'

    license = 'BSL-1.0'
    description = '''Design pattern to manage large quantities of highly redundant objects.'''
    author = 'Joaquín M López Muñoz'
    url = 'https://github.com/boostorg/flyweight.git'
    topics = ['Patterns']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'