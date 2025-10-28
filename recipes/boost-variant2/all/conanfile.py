from conan import ConanFile


class BoostVariant2Recipe(ConanFile):
    name = 'boost-variant2'

    license = 'BSL-1.0'
    description = '''A never-valueless, strong guarantee implementation of std::variant.'''
    author = 'Peter Dimov'
    url = 'https://github.com/boostorg/variant2.git'
    topics = ['Containers', 'Data']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'