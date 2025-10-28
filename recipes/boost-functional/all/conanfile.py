from conan import ConanFile


class BoostFunctionalRecipe(ConanFile):
    name = 'boost-functional'

    license = 'BSL-1.0'
    description = '''The Boost.Function library contains a family of class templates that are function object wrappers.'''
    author = 'Mark Rodgers'
    url = 'https://github.com/boostorg/functional.git'
    topics = ['Function-objects']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'