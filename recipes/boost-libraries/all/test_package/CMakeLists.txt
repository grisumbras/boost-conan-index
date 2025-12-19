cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

find_package(Boost CONFIG REQUIRED)

add_executable(test_program test.cpp)
target_link_libraries(test_program PRIVATE Boost::headers)

include(CTest)
add_test(NAME test COMMAND test_program)