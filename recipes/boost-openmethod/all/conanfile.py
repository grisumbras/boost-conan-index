from conan import ConanFile


class BoostOpenmethodRecipe(ConanFile):
    name = 'boost-openmethod'

    license = 'BSL-1.0'
    description = '''Open-methods are virtual functions that exist outside of classes, as free-standing functions. They make it possible to add polymorphic behavior to existing classes, without modifying them. This implementation supports single and multiple dispatch.'''
    author = 'Jean-Louis Leroy'
    url = 'https://github.com/boostorg/openmethod.git'
    topics = ['Emulation', 'Programming']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'