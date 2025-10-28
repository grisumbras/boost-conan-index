from conan import ConanFile


class BoostUuidRecipe(ConanFile):
    name = 'boost-uuid'

    license = 'BSL-1.0'
    description = '''A universally unique identifier.'''
    author = 'Andy Tompkins'
    url = 'https://github.com/boostorg/uuid.git'
    topics = ['Data', 'Domain']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'