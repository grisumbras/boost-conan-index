from conan import ConanFile


class BoostJsonRecipe(ConanFile):
    name = 'boost-json'

    license = 'BSL-1.0'
    description = '''JSON parsing, serialization, and DOM in C++11'''
    author = 'Vinnie Falco, Krystian Stasiowski'
    url = 'https://github.com/boostorg/json.git'
    topics = ['Containers', 'Data', 'IO']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'