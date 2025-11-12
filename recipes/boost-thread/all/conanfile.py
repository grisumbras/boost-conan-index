from conan import ConanFile


class BoostThreadRecipe(ConanFile):
    name = 'boost-thread'

    license = 'BSL-1.0'
    description = '''Portable C++ multi-threading. C++11, C++14, C++17.'''
    author = 'Anthony Williams, Vicente J. Botet Escriba'
    url = 'https://github.com/boostorg/thread.git'
    topics = ['Concurrent', 'System']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'