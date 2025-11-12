from conan import ConanFile


class BoostGilRecipe(ConanFile):
    name = 'boost-gil'

    license = 'BSL-1.0'
    description = '''(C++14) Generic Image Library'''
    author = 'Lubomir Bourdev, Hailin Jin, Christian Henning'
    url = 'https://github.com/boostorg/gil.git'
    topics = ['Algorithms', 'Containers', 'Generic', 'Image-processing', 'Iterators']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'