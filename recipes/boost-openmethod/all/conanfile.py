from conan import ConanFile


class BoostOpenmethodRecipe(ConanFile):
    name = 'boost-openmethod'

    license = 'BSL-1.0'
    description = '''Open-methods are free-standing functions that work like virtual functions: they select the b​est overrider from a set, depending on the dynamic type of their arguments. This makes it possible to add polymorphic operations to existing classes, without modifying them. They make patterns like Visitor unnecessary.'''
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