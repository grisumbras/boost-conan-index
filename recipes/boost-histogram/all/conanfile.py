from conan import ConanFile


class BoostHistogramRecipe(ConanFile):
    name = 'boost-histogram'

    license = 'BSL-1.0'
    description = '''Fast multi-dimensional histogram with convenient interface for C++14'''
    author = 'Hans Dembinski'
    url = 'https://github.com/boostorg/histogram.git'
    topics = ['Algorithms', 'Data', 'Math']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'