from conan import ConanFile


class BoostTestRecipe(ConanFile):
    name = 'boost-test'

    license = 'BSL-1.0'
    description = '''Support for simple program testing, full unit testing, and for program execution monitoring.'''
    author = 'Gennadiy Rozental, Raffi Enficiaud'
    url = 'https://github.com/boostorg/test.git'
    topics = ['Correctness']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'