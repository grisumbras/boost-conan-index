from conan import ConanFile


class BoostDescribeRecipe(ConanFile):
    name = 'boost-describe'

    license = 'BSL-1.0'
    description = '''A C++14 reflection library.'''
    author = 'Peter Dimov'
    url = 'https://github.com/boostorg/describe.git'
    topics = ['Emulation', 'Metaprogramming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'