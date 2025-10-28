from conan import ConanFile


class BoostTimerRecipe(ConanFile):
    name = 'boost-timer'

    license = 'BSL-1.0'
    description = '''Event timer, progress timer, and progress display classes.'''
    author = 'Beman Dawes'
    url = 'https://github.com/boostorg/timer.git'
    topics = ['Miscellaneous']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'