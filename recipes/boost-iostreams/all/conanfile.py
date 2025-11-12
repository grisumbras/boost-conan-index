from conan import ConanFile


class BoostIostreamsRecipe(ConanFile):
    name = 'boost-iostreams'

    license = 'BSL-1.0'
    description = '''Boost.IOStreams provides a framework for defining streams, stream buffers and i/o filters.'''
    author = 'Jonathan Turkanis'
    url = 'https://github.com/boostorg/iostreams.git'
    topics = ['IO', 'String']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'