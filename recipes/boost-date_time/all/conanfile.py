from conan import ConanFile


class BoostDateTimeRecipe(ConanFile):
    name = 'boost-date_time'

    license = 'BSL-1.0'
    description = '''A set of date-time libraries based on generic programming concepts.'''
    author = 'Jeff Garland'
    url = 'https://github.com/boostorg/date_time.git'
    topics = ['Domain', 'System']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'