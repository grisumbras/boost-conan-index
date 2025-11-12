from conan import ConanFile


class BoostConfigRecipe(ConanFile):
    name = 'boost-config'

    license = 'BSL-1.0'
    description = '''Helps Boost library developers adapt to compiler idiosyncrasies; not intended for library users.'''
    author = ''
    url = 'https://github.com/boostorg/config.git'
    topics = ['Workarounds']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'