from conan import ConanFile


class BoostSafeNumericsRecipe(ConanFile):
    name = 'boost-safe_numerics'

    license = 'BSL-1.0'
    description = '''Guaranteed Correct Integer Arithmetic'''
    author = 'Robert Ramey'
    url = 'https://github.com/boostorg/safe_numerics.git'
    topics = ['Math', 'Correctness']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'