from conan import ConanFile


class BoostOpenmethodRecipe(ConanFile):
    name = 'boost-openmethod'

    license = 'BSL-1.0'
    description = '''Open methods for C++17 and above.'''
    author = 'Jean-Louis Leroy'
    url = 'https://github.com/boostorg/openmethod.git'
    topics = ['Programming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'