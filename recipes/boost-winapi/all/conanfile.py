from conan import ConanFile


class BoostWinapiRecipe(ConanFile):
    name = 'boost-winapi'

    license = 'BSL-1.0'
    description = '''Windows API abstraction layer.'''
    author = 'Peter Dimov, Vicente J. Botet Escriba, Andrey Semashev'
    url = 'https://github.com/boostorg/winapi.git'
    topics = ['Miscellaneous']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'