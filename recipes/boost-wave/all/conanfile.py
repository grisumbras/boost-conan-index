from conan import ConanFile


class BoostWaveRecipe(ConanFile):
    name = 'boost-wave'

    license = 'BSL-1.0'
    description = '''The Boost.Wave library is a Standards conformant, and highly configurable implementation of the mandated C99/C++ preprocessor functionality packed behind an easy to use iterator interface.'''
    author = 'Hartmut Kaiser'
    url = 'https://github.com/boostorg/wave.git'
    topics = ['String']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'