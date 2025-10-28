from conan import ConanFile


class BoostMsmRecipe(ConanFile):
    name = 'boost-msm'

    license = 'BSL-1.0'
    description = '''A very high-performance library for expressive UML2 finite state machines.'''
    author = 'Christophe Henry'
    url = 'https://github.com/boostorg/msm.git'
    topics = ['State']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'