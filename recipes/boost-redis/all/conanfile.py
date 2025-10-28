from conan import ConanFile


class BoostRedisRecipe(ConanFile):
    name = 'boost-redis'

    license = 'BSL-1.0'
    description = '''Redis async client library built on top of Boost.Asio.'''
    author = 'Marcelo Zimbres Silva'
    url = 'https://github.com/boostorg/redis.git'
    topics = ['Concurrent', 'IO']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'