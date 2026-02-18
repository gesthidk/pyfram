cmake_minimum_required(VERSION 3.15)
project(TestProject)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Download pybind11
include(FetchContent)
FetchContent_Declare(
    pybind11
    URL https://github.com/pybind/pybind11/archive/v2.10.4.zip
)
FetchContent_MakeAvailable(pybind11)

#Find Eigen

find_package(Eigen3 REQUIRED)

# Create static library
add_library(tensor STATIC
    cpp_modules/tensor.cpp
)

set_target_properties(tensor PROPERTIES POSITION_INDEPENDENT_CODE ON)

target_include_directories(tensor PUBLIC cpp_modules)

target_link_libraries(tensor PRIVATE Eigen3::Eigen)

# Create Python extension module using pybind11
pybind11_add_module(tensor_py
    cpp_modules/tensor_py.cpp
)

set_target_properties(tensor_py PROPERTIES PREFIX "" SUFFIX ".so")

# Set output directory for Python module
set_target_properties(tensor_py PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
)

target_link_libraries(tensor_py PRIVATE tensor)
