from conan import ConanFile


class BoostProgramOptionsRecipe(ConanFile):
    name = 'boost-program_options'

    license = 'BSL-1.0'
    description = '''The program_options library allows program developers to obtain program options, that is (name, value) pairs from the user, via conventional methods such as command line and config file.'''
    author = 'Vladimir Prus'
    url = 'https://github.com/boostorg/program_options.git'
    topics = ['IO', 'Miscellaneous']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'