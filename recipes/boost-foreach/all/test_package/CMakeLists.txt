cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

set(Boost_USE_MULTITHREADED  OFF)
set(Boost_USE_STATIC_LIBS ON)
set(Boost_ARCHITECTURE)
find_package(boost-foreach CONFIG REQUIRED)

add_executable(test_program test.cpp)
target_link_libraries(test_program Boost::foreach)

if("foreach" STREQUAL python)
    find_package(Python COMPONENTS Development REQUIRED)
    target_link_libraries(test_program Python::Python)
endif()

include(CTest)
add_test(NAME test COMMAND test_program)