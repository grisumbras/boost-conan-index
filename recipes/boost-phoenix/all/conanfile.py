from conan import ConanFile


class BoostPhoenixRecipe(ConanFile):
    name = 'boost-phoenix'

    license = 'BSL-1.0'
    description = '''Define small unnamed function objects at the actual call site, and more.'''
    author = 'Joel de Guzman, Dan Marsden, Thomas Heller, John Fletcher'
    url = 'https://github.com/boostorg/phoenix.git'
    topics = ['Function-objects']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'