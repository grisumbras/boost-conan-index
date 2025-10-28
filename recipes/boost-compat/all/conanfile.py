from conan import ConanFile


class BoostCompatRecipe(ConanFile):
    name = 'boost-compat'

    license = 'BSL-1.0'
    description = '''C++11 implementations of standard components added in later C++ standards.'''
    author = 'Peter Dimov, Christian Mazakas'
    url = 'https://github.com/boostorg/compat.git'
    topics = ['Emulation', 'Programming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'