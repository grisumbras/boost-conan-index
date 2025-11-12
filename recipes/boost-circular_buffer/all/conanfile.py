from conan import ConanFile


class BoostCircularBufferRecipe(ConanFile):
    name = 'boost-circular_buffer'

    license = 'BSL-1.0'
    description = '''A STL compliant container also known as ring or cyclic buffer.'''
    author = 'Jan Gaspar'
    url = 'https://github.com/boostorg/circular_buffer.git'
    topics = ['Containers']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'