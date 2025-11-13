import os

from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.build import can_run


class BoostFunctionTestConan(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'CMakeDeps', 'CMakeToolchain'

    def requirements(self):
        self.requires(self.tested_reference_str)

    def generate(self):
        cmake = CMake(self)
        cmake.configure()

    def build(self):
        cmake = CMake(self)
        cmake.build()

    def layout(self):
        cmake_layout(self)

    def test(self):
        if can_run(self):
            cmake = CMake(self)
            cmake.test()