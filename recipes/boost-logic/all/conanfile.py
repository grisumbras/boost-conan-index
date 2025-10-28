from conan import ConanFile


class BoostLogicRecipe(ConanFile):
    name = 'boost-logic'

    license = 'BSL-1.0'
    description = '''3-state boolean type library.'''
    author = 'Doug Gregor'
    url = 'https://github.com/boostorg/logic.git'
    topics = ['Miscellaneous']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'