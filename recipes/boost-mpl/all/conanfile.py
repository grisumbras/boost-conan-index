from conan import ConanFile


class BoostMplRecipe(ConanFile):
    name = 'boost-mpl'

    license = 'BSL-1.0'
    description = '''The Boost.MPL library is a general-purpose, high-level C++ template metaprogramming framework of compile-time algorithms, sequences and metafunctions. It provides a conceptual foundation and an extensive set of powerful and coherent tools that make doing explict metaprogramming in C++ as easy and enjoyable as possible within the current language.'''
    author = 'Aleksey Gurtovoy'
    url = 'https://github.com/boostorg/mpl.git'
    topics = ['Metaprogramming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'