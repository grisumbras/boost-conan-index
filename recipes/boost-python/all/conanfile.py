from conan import ConanFile


class BoostPythonRecipe(ConanFile):
    name = 'boost-python'

    license = 'BSL-1.0'
    description = '''The Boost Python Library is a framework for interfacing Python and C++. It allows you to quickly and seamlessly expose C++ classes functions and objects to Python, and vice-versa, using no special tools -- just your C++ compiler.'''
    author = 'Dave Abrahams'
    url = 'https://github.com/boostorg/python.git'
    topics = ['Inter-language']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'