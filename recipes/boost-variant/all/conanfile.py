from conan import ConanFile


class BoostVariantRecipe(ConanFile):
    name = 'boost-variant'

    license = 'BSL-1.0'
    description = '''Safe, generic, stack-based discriminated union container.'''
    author = 'Eric Friedman, Itay Maman'
    url = 'https://github.com/boostorg/variant.git'
    topics = ['Containers', 'Data']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'