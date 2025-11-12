from conan import ConanFile


class BoostComputeRecipe(ConanFile):
    name = 'boost-compute'

    license = 'BSL-1.0'
    description = '''Parallel/GPU-computing library'''
    author = 'Kyle Lutz'
    url = 'https://github.com/boostorg/compute.git'
    topics = ['Concurrent']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'