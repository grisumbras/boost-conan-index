from conan import ConanFile


class BoostMetaparseRecipe(ConanFile):
    name = 'boost-metaparse'

    license = 'BSL-1.0'
    description = '''A library for generating compile time parsers parsing embedded DSL code as part of the C++ compilation process'''
    author = 'Abel Sinkovics'
    url = 'https://github.com/boostorg/metaparse.git'
    topics = ['Metaprogramming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'