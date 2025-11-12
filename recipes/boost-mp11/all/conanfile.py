from conan import ConanFile


class BoostMp11Recipe(ConanFile):
    name = 'boost-mp11'

    license = 'BSL-1.0'
    description = '''A C++11 metaprogramming library.'''
    author = 'Peter Dimov'
    url = 'https://github.com/boostorg/mp11.git'
    topics = ['Metaprogramming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'