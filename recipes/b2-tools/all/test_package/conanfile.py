import os

from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.build import can_run


class BoostB2GeneratorsTestConan(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    python_requires = 'tested_reference_str'
    requires = 'boost-json/[>0-a,include_prerelease]'

    def build_requirements(self):
       self.tool_requires('b2/[>=5.3.0]')

    def generate(self):
        b2_gens = self.python_requires['b2-tools'].module

        tc = b2_gens.B2Toolchain(self)
        tc.generate()

        deps = b2_gens.B2Deps(self)
        deps.generate()

    def build(self):
        b2 = self.python_requires['b2-tools'].module.B2(self)
        b2.build()

    def test(self):
        if not can_run(self):
            return
        b2 = self.python_requires['b2-tools'].module.B2(self)
        b2.build('run')