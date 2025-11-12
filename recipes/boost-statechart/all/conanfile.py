from conan import ConanFile


class BoostStatechartRecipe(ConanFile):
    name = 'boost-statechart'

    license = 'BSL-1.0'
    description = '''Boost.Statechart - Arbitrarily complex finite state machines can be implemented in easily readable and maintainable C++ code.'''
    author = 'Andreas Huber Dönni'
    url = 'https://github.com/boostorg/statechart.git'
    topics = ['State']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'