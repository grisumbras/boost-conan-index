from conan import ConanFile


class BoostUnitsRecipe(ConanFile):
    name = 'boost-units'

    license = 'BSL-1.0'
    description = '''Zero-overhead dimensional analysis and unit/quantity manipulation and conversion.'''
    author = 'Matthias Schabel, Steven Watanabe'
    url = 'https://github.com/boostorg/units.git'
    topics = ['Domain']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'