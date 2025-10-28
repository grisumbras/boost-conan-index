from conan import ConanFile


class BoostRatioRecipe(ConanFile):
    name = 'boost-ratio'

    license = 'BSL-1.0'
    description = '''Compile time rational arithmetic. C++11.'''
    author = 'Howard Hinnant, Beman Dawes, Vicente J. Botet Escriba'
    url = 'https://github.com/boostorg/ratio.git'
    topics = ['Math']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'