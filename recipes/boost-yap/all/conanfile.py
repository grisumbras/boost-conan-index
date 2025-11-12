from conan import ConanFile


class BoostYapRecipe(ConanFile):
    name = 'boost-yap'

    license = 'BSL-1.0'
    description = '''An expression template library for C++14 and later.'''
    author = 'T. Zachary Laine'
    url = 'https://github.com/boostorg/yap.git'
    topics = ['Generic', 'Metaprogramming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'