from conan import ConanFile


class BoostBindRecipe(ConanFile):
    name = 'boost-bind'

    license = 'BSL-1.0'
    description = '''boost::bind is a generalization of the standard functions std::bind1st and std::bind2nd. It supports arbitrary function objects, functions, function pointers, and member function pointers, and is able to bind any argument to a specific value or route input arguments into arbitrary positions.'''
    author = 'Peter Dimov'
    url = 'https://github.com/boostorg/bind.git'
    topics = ['Function-objects']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'