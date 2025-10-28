from conan import ConanFile


class BoostTypeofRecipe(ConanFile):
    name = 'boost-typeof'

    license = 'BSL-1.0'
    description = '''Typeof operator emulation.'''
    author = 'Arkadiy Vertleyb, Peder Holt'
    url = 'https://github.com/boostorg/typeof.git'
    topics = ['Emulation']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'