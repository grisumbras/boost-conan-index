cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

set(Boost_USE_MULTITHREADED  OFF)
set(Boost_USE_STATIC_LIBS ON)
set(Boost_ARCHITECTURE)
find_package(boost-iterator CONFIG REQUIRED)

add_executable(test_program test.cpp)
target_link_libraries(test_program Boost::iterator)



include(CTest)
add_test(NAME test COMMAND test_program)