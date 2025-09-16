cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

find_package(boost-assert CONFIG REQUIRED)

add_executable(test test.cpp)
target_link_libraries(test Boost::Assert)