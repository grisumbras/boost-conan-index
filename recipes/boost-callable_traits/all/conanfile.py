from conan import ConanFile


class BoostCallableTraitsRecipe(ConanFile):
    name = 'boost-callable_traits'

    license = 'BSL-1.0'
    description = '''A spiritual successor to Boost.FunctionTypes, Boost.CallableTraits is a header-only C++11 library for the compile-time inspection and manipulation of all 'callable' types. Additional support for C++17 features.'''
    author = 'Barrett Adair'
    url = 'https://github.com/boostorg/callable_traits.git'
    topics = ['Metaprogramming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'