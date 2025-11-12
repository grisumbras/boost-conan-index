from conan import ConanFile


class BoostTupleRecipe(ConanFile):
    name = 'boost-tuple'

    license = 'BSL-1.0'
    description = '''Ease definition of functions returning multiple values, and more.'''
    author = 'Jaakko Järvi'
    url = 'https://github.com/boostorg/tuple.git'
    topics = ['Data']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'