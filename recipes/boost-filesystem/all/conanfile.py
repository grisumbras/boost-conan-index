from conan import ConanFile


class BoostFilesystemRecipe(ConanFile):
    name = 'boost-filesystem'

    license = 'BSL-1.0'
    description = '''The Boost Filesystem Library provides portable facilities to query and manipulate paths, files, and directories.'''
    author = 'Beman Dawes'
    url = 'https://github.com/boostorg/filesystem.git'
    topics = ['System']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'