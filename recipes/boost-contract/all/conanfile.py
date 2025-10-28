from conan import ConanFile


class BoostContractRecipe(ConanFile):
    name = 'boost-contract'

    license = 'BSL-1.0'
    description = '''Contract programming for C++. All contract programming features are supported: Subcontracting, class invariants, postconditions (with old and return values), preconditions, customizable actions on assertion failure (e.g., terminate or throw), optional compilation and checking of assertions, etc.'''
    author = 'Lorenzo Caminiti'
    url = 'https://github.com/boostorg/contract.git'
    topics = ['Correctness']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = {'shared': False}
    python_requires = (
        'b2-tools/0.0.1-a',
        'boost-helpers/0.0.1-a',
    )
    python_requires_extend = 'boost-helpers.BoostPackage'