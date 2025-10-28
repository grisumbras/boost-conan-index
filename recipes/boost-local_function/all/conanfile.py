from conan import ConanFile


class BoostLocalFunctionRecipe(ConanFile):
    name = 'boost-local_function'

    license = 'BSL-1.0'
    description = '''Program functions locally, within other functions, directly within the scope where they are needed.'''
    author = 'Lorenzo Caminiti'
    url = 'https://github.com/boostorg/local_function.git'
    topics = ['Function-objects']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'