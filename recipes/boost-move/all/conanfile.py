from conan import ConanFile


class BoostMoveRecipe(ConanFile):
    name = 'boost-move'

    license = 'BSL-1.0'
    description = '''Portable move semantics for C++03 and C++11 compilers.'''
    author = 'Ion Gaztañaga'
    url = 'https://github.com/boostorg/move.git'
    topics = ['Emulation']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'