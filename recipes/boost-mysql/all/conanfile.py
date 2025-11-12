from conan import ConanFile


class BoostMysqlRecipe(ConanFile):
    name = 'boost-mysql'

    license = 'BSL-1.0'
    description = '''MySQL client library built on top of Boost.Asio.'''
    author = 'Rubén Pérez'
    url = 'https://github.com/boostorg/mysql.git'
    topics = ['Concurrent', 'IO']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'