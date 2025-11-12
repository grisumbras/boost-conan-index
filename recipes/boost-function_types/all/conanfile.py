from conan import ConanFile


class BoostFunctionTypesRecipe(ConanFile):
    name = 'boost-function_types'

    license = 'BSL-1.0'
    description = '''Boost.FunctionTypes provides functionality to classify, decompose and synthesize function, function pointer, function reference and pointer to member types.'''
    author = 'Tobias Schwinger'
    url = 'https://github.com/boostorg/function_types.git'
    topics = ['Generic', 'Metaprogramming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'