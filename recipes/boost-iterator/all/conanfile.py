from conan import ConanFile


class BoostIteratorRecipe(ConanFile):
    name = 'boost-iterator'

    license = 'BSL-1.0'
    description = '''The Boost Iterator Library contains two parts. The first is a system of concepts which extend the C++ standard iterator requirements. The second is a framework of components for building iterators based on these extended concepts and includes several useful iterator adaptors.'''
    author = 'Dave Abrahams, Jeremy Siek, Thomas Witt'
    url = 'https://github.com/boostorg/iterator.git'
    topics = ['Iterators']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'