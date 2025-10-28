from conan import ConanFile


class BoostTypeIndexRecipe(ConanFile):
    name = 'boost-type_index'

    license = 'BSL-1.0'
    description = '''Runtime/Compile time copyable type info.'''
    author = 'Antony Polukhin'
    url = 'https://github.com/boostorg/type_index.git'
    topics = ['Emulation']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'