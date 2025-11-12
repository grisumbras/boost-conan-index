from conan import ConanFile


class BoostParameterPythonRecipe(ConanFile):
    name = 'boost-parameter_python'

    license = 'BSL-1.0'
    description = '''Boost.Parameter Library Python bindings.'''
    author = 'David Abrahams, Daniel Wallin'
    url = 'https://github.com/boostorg/parameter_python.git'
    topics = ['Emulation', 'Programming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'