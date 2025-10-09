cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

set(Boost_USE_MULTITHREADED  OFF)
set(Boost_USE_STATIC_LIBS ON)
set(Boost_ARCHITECTURE)
find_package(boost-random CONFIG REQUIRED)

add_executable(test test.cpp)
target_link_libraries(test Boost::random)