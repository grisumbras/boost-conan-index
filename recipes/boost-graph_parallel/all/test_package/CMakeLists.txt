cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

set(Boost_USE_MULTITHREADED  OFF)
set(Boost_USE_STATIC_LIBS ON)
set(Boost_ARCHITECTURE)
find_package(boost-graph_parallel CONFIG REQUIRED)

add_executable(test_program test.cpp)
target_link_libraries(test_program PRIVATE

    Boost::graph_parallel

)



find_package(MPI COMPONENTS CXX REQUIRED)
target_link_libraries(test_program PRIVATE MPI::MPI_CXX)




include(CTest)
add_test(NAME test COMMAND test_program)