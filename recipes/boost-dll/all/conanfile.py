from conan import ConanFile


class BoostDllRecipe(ConanFile):
    name = 'boost-dll'

    license = 'BSL-1.0'
    description = '''Library for comfortable work with DLL and DSO.'''
    author = 'Antony Polukhin, Renato Tegon Forti'
    url = 'https://github.com/boostorg/dll.git'
    topics = ['System']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'