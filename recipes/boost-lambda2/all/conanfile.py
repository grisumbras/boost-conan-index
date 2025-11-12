from conan import ConanFile


class BoostLambda2Recipe(ConanFile):
    name = 'boost-lambda2'

    license = 'BSL-1.0'
    description = '''A C++14 lambda library.'''
    author = 'Peter Dimov'
    url = 'https://github.com/boostorg/lambda2.git'
    topics = ['Function-objects']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'