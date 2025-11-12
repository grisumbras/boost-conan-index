from conan import ConanFile


class BoostProcessRecipe(ConanFile):
    name = 'boost-process'

    license = 'BSL-1.0'
    description = '''Library to create processes in a portable way.'''
    author = 'Merino Vidal, Ilya Sokolov, Felipe Tanus, Jeff Flinn, Thomas Jarosch, Boris Schaeling, Klemens D. Morgenstern'
    url = 'https://github.com/boostorg/process.git'
    topics = ['System']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'