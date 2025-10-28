from conan import ConanFile


class BoostOdeintRecipe(ConanFile):
    name = 'boost-odeint'

    license = 'BSL-1.0'
    description = '''Solving ordinary differential equations.'''
    author = 'Karsten Ahnert, Mario Mulansky'
    url = 'https://github.com/boostorg/odeint.git'
    topics = ['Math']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'