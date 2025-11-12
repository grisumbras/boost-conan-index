from conan import ConanFile


class BoostSmartPtrRecipe(ConanFile):
    name = 'boost-smart_ptr'

    license = 'BSL-1.0'
    description = '''Smart pointer class templates.'''
    author = 'Greg Colvin, Beman Dawes, Peter Dimov, Darin Adler, Glen Fernandes'
    url = 'https://github.com/boostorg/smart_ptr.git'
    topics = ['Memory']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'