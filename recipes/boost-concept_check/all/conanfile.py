from conan import ConanFile


class BoostConceptCheckRecipe(ConanFile):
    name = 'boost-concept_check'

    license = 'BSL-1.0'
    description = '''Tools for generic programming.'''
    author = 'Jeremy Siek'
    url = 'https://github.com/boostorg/concept_check.git'
    topics = ['Correctness', 'Generic']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'disabled_libraries': ['ANY']}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'