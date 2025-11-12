from conan import ConanFile


class BoostUrlRecipe(ConanFile):
    name = 'boost-url'

    license = 'BSL-1.0'
    description = '''URL parsing in C++11'''
    author = 'Vinnie Falco, Alan de Freitas'
    url = 'https://github.com/boostorg/url.git'
    topics = ['Containers', 'Data', 'IO']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'