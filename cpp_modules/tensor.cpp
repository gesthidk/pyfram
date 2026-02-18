#include "tensor.h"
#include <Eigen/Dense>

double Tensor3x3::trace() const {
        return data_[0] + data_[4] + data_[8];
}
double Tensor3x3::determinant() const {
        return
            data_[0]*(data_[4]*data_[8] - data_[5]*data_[7])
          - data_[1]*(data_[3]*data_[8] - data_[5]*data_[6])
          + data_[2]*(data_[3]*data_[7] - data_[4]*data_[6]);
}
double Tensor3x3::doubleContraction(const Tensor3x3& B) const {
        double sum = 0.0;
        for(int i=0;i<9;i++)
            sum += data_[i] * B.data_[i];
        return sum;
}

//Matrix multiplication
Tensor3x3 Tensor3x3::operator*(const Tensor3x3& B) const {
        Tensor3x3 C;

        for(int i=0;i<3;i++)
            for(int j=0;j<3;j++)
                for(int k=0;k<3;k++)
                    C(i,j) += (*this)(i,k) * B(k,j);

        return C;
}
Tensor3x3 Tensor3x3::transpose() const {
        Tensor3x3 T;

        for(int i=0;i<3;i++)
            for(int j=0;j<3;j++)
                T(i,j) = (*this)(j,i);

        return T;
}

Tensor3x3 Tensor3x3::rotate(const Tensor3x3& R) const {
        return R * (*this) * R.transpose();
}

std::array<double, 3> Tensor3x3::eigenvalues() const {
    Eigen::Matrix3d mat;
    for(int i=0;i<3;i++)
        for(int j=0;j<3;j++)
            mat(i,j) = (*this)(i,j);

    Eigen::SelfAdjointEigenSolver<Eigen::Matrix3d> solver(mat);
    if(solver.info() != Eigen::Success)
        throw std::runtime_error("Eigenvalue computation failed");

    Eigen::Vector3d eigs = solver.eigenvalues();
    return {eigs[0], eigs[1], eigs[2]};
}

Tensor3x3 Tensor3x3::deviatoric() const {
    Tensor3x3 dev = *this;
    double tr = trace();
    for(int i=0;i<3;i++)
        dev(i,i) -= tr/3.0;
    return dev;
}

double Tensor3x3::J2() const {
    Tensor3x3 dev = deviatoric();
    return 0.5 * dev.doubleContraction(dev);
}

