from conan import ConanFile


class BoostUtilityRecipe(ConanFile):
    name = 'boost-utility'

    license = 'BSL-1.0'
    description = '''Various utilities, such as base-from-member idiom and binary literals in C++03.'''
    author = 'Dave Abrahams and others'
    url = 'https://github.com/boostorg/utility.git'
    topics = ['Miscellaneous', 'Patterns']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'