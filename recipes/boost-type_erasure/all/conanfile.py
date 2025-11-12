from conan import ConanFile


class BoostTypeErasureRecipe(ConanFile):
    name = 'boost-type_erasure'

    license = 'BSL-1.0'
    description = '''Runtime polymorphism based on concepts.'''
    author = 'Steven Watanabe'
    url = 'https://github.com/boostorg/type_erasure.git'
    topics = ['Data']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'