#pragma once
#include <array>
#include <cmath>
#include <stdexcept>

class Tensor3x3 {
private:
    std::array<double, 9> data_;

public:
    double trace() const;
    double determinant() const;
    double doubleContraction(const Tensor3x3& B) const;
    Tensor3x3 operator*(const Tensor3x3& B) const;
    Tensor3x3 transpose()const;
    Tensor3x3 rotate(const Tensor3x3& R) const;

    Tensor3x3() {
        data_.fill(0.0);
    }

    Tensor3x3(const std::array<double,9>& values)
        : data_(values) {}

    double& operator()(int i, int j) {
        return data_[i*3 + j];
    }

    double operator()(int i, int j) const {
        return data_[i*3 + j];
    }

    const std::array<double,9>& data() const {
        return data_;
    }

    static Tensor3x3 Identity() {
        return Tensor3x3({
            1,0,0,
            0,1,0,
            0,0,1
        });
    }

   // Tensor3x3(const std::vector<double>&); // constructor from flat list of 9

    std::array<double, 3> eigenvalues() const;

    Tensor3x3 deviatoric() const;

    double J2() const;

};
