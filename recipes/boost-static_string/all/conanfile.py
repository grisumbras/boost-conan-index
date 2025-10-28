from conan import ConanFile


class BoostStaticStringRecipe(ConanFile):
    name = 'boost-static_string'

    license = 'BSL-1.0'
    description = '''A fixed capacity dynamically sized string.'''
    author = 'Krystian Stasiowski, Vinnie Falco'
    url = 'https://github.com/boostorg/static_string.git'
    topics = ['Container', 'String']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'