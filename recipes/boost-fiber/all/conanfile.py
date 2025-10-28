from conan import ConanFile


class BoostFiberRecipe(ConanFile):
    name = 'boost-fiber'

    license = 'BSL-1.0'
    description = '''(C++11) Userland threads library.'''
    author = 'Oliver Kowalke'
    url = 'https://github.com/boostorg/fiber.git'
    topics = ['Concurrent', 'System']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'