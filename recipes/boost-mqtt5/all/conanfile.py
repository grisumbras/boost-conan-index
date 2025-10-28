from conan import ConanFile


class BoostMqtt5Recipe(ConanFile):
    name = 'boost-mqtt5'

    license = 'BSL-1.0'
    description = '''MQTT5 client library built on top of Boost.Asio.'''
    author = 'Ivica Siladić, Bruno Iljazović, Korina Šimičević'
    url = 'https://github.com/boostorg/mqtt5.git'
    topics = ['Concurrent', 'IO']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'