from conan import ConanFile


class BoostPredefRecipe(ConanFile):
    name = 'boost-predef'

    license = 'BSL-1.0'
    description = '''This library defines a set of compiler, architecture, operating system, library, and other version numbers from the information it can gather of C, C++, Objective C, and Objective C++ predefined macros or those defined in generally available headers.'''
    author = 'René Ferdinand Rivera Morell'
    url = 'https://github.com/boostorg/predef.git'
    topics = ['Miscellaneous']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'