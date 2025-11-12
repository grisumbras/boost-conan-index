from conan import ConanFile


class BoostIclRecipe(ConanFile):
    name = 'boost-icl'

    license = 'BSL-1.0'
    description = '''Interval Container Library, interval sets and maps and aggregation of associated values'''
    author = 'Joachim Faulhaber'
    url = 'https://github.com/boostorg/icl.git'
    topics = ['Containers', 'Data']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'