#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <utility>
#include "tensor.h"


PYBIND11_MODULE(tensor_py, m){

    pybind11::class_<Tensor3x3>(m,"Tensor3x3")
        .def(pybind11::init<>())
        .def(pybind11::init<const std::array<double,9>&>())
        .def("trace", &Tensor3x3::trace)
        .def("determinant", &Tensor3x3::determinant)
        .def("doubleContraction", &Tensor3x3::doubleContraction)
        .def("transpose", &Tensor3x3::transpose)
        .def("rotate", &Tensor3x3::rotate)
        .def("eigenvalues", &Tensor3x3::eigenvalues)   // expose eigenvalues
        .def("deviatoric", &Tensor3x3::deviatoric)    // expose deviatoric
        .def("J2", &Tensor3x3::J2)       
        .def("__mul__", &Tensor3x3::operator*)
        // Indexing
        .def("__getitem__", [](const Tensor3x3 &t, std::pair<int,int> idx) {
            return t(idx.first, idx.second);
         })
        .def("__setitem__", [](Tensor3x3 &t, std::pair<int,int> idx, double value) {
            t(idx.first, idx.second) = value;
         });
};
