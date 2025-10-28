from conan import ConanFile


class BoostStacktraceRecipe(ConanFile):
    name = 'boost-stacktrace'

    license = 'BSL-1.0'
    description = '''Gather, store, copy and print backtraces.'''
    author = 'Antony Polukhin'
    url = 'https://github.com/boostorg/stacktrace.git'
    topics = ['System', 'Correctness']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'