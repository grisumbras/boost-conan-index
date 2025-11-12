from conan import ConanFile


class BoostContextRecipe(ConanFile):
    name = 'boost-context'

    license = 'BSL-1.0'
    description = '''(C++11) Context switching library.'''
    author = 'Oliver Kowalke'
    url = 'https://github.com/boostorg/context.git'
    topics = ['Concurrent', 'System']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'