import subprocess
import importlib.util
from pathlib import Path
import pytest
import sys
import numpy as np

@pytest.fixture(scope="session", autouse=True)
def build_cpp_extension():
    """Build C++ extension with pybind11 before running tests"""
    
    root = Path(__file__).parent.parent
    build_dir = root / "build"
    
    print("\n" + "="*60)
    print("Building C++ extension with pybind11...")
    print("="*60)
    
    # Create build directory
    build_dir.mkdir(exist_ok=True)
    
    # Run cmake
    print("\n[1/2] Running cmake...")
    cmake_result = subprocess.run(
        ["cmake", ".."],
        cwd=build_dir,
        capture_output=True,
        text=True
    )
    
    if cmake_result.returncode != 0:
        print("❌ CMAKE FAILED")
        print("\nSTDOUT:")
        print(cmake_result.stdout)
        print("\nSTDERR:")
        print(cmake_result.stderr)
        raise RuntimeError("CMake configuration failed")
    
    print("✅ CMake successful")
    
    # Run make with VERBOSE output
    print("\n[2/2] Running make...")
    make_result = subprocess.run(
        ["make", "VERBOSE=1"],  # Added VERBOSE=1 to see compilation details
        cwd=build_dir,
        capture_output=True,
        text=True
    )
    
    if make_result.returncode != 0:
        print("❌ MAKE FAILED")
        print("\n" + "="*60)
        print("COMPILATION ERROR - STDOUT:")
        print("="*60)
        print(make_result.stdout)
        print("\n" + "="*60)
        print("COMPILATION ERROR - STDERR:")
        print("="*60)
        print(make_result.stderr)
        print("="*60)
        raise RuntimeError("Build failed - see errors above")

    print("✅ Build successful")

@pytest.fixture(scope="session")
def tensor_module(build_cpp_extension):
    root = Path(__file__).parent.parent
    build_dir = root / "build"
    so_file = build_dir / "tensor_py.so"
    if not so_file.exists():
        raise FileNotFoundError(f"{so_file} not found!")


    spec = importlib.util.spec_from_file_location("tensor_py", so_file)
    tensor_py = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tensor_py)
    return tensor_py



def random_tensor(scale=1.0):
    return np.random.randn(3, 3) * scale


def symmetric_tensor(scale=1.0):
    A = random_tensor(scale)
    return 0.5 * (A + A.T)


def to_tensor_cpp(A_np , tensor_module):
    T = tensor_module.Tensor3x3()
    for i in range(3):
        for j in range(3):
            T[i, j] = float(A_np[i, j])
    return T


def test_zero_trace(tensor_module):
    T = tensor_module.Tensor3x3()
    assert T.trace() == pytest.approx(0.0)


def test_identity_det(tensor_module):
    I = np.eye(3)
    T = tensor_module.Tensor3x3(I.flatten().tolist())
    assert T.determinant() == pytest.approx(1.0)

def test_trace_equals_numpy(tensor_module):
    A = random_tensor()
    T = tensor_module.Tensor3x3(A.flatten().tolist())
    assert T.trace() == pytest.approx(np.trace(A))

def test_det_matches_numpy(tensor_module):
    A = random_tensor()
    T = tensor_module.Tensor3x3(A.flatten().tolist())
    assert T.determinant() == pytest.approx(np.linalg.det(A), rel=1e-6)


def test_eigenvalues_match_numpy(tensor_module):
    A = symmetric_tensor()
    T = tensor_module.Tensor3x3(A.flatten().tolist())

    eig_np = np.linalg.eigvalsh(A)  # sorted
    eig_cpp = sorted(T.eigenvalues())

    assert eig_cpp == pytest.approx(eig_np, rel=1e-6)

def test_eigenvalues_sorted(tensor_module):
    A = symmetric_tensor()
    T = tensor_module.Tensor3x3(A.flatten().tolist())
    eig = T.eigenvalues()

    assert eig[0] <= eig[1] <= eig[2]

def test_deviatoric_trace_zero(tensor_module):
    A = random_tensor()
    T = tensor_module.Tensor3x3(A.flatten().tolist())

    dev = T.deviatoric()
    assert dev.trace() == pytest.approx(0.0, abs=1e-10)

def test_double_contraction(tensor_module):
    A = random_tensor()
    T = tensor_module.Tensor3x3(A.flatten().tolist())

    dc = T.doubleContraction(T)
    frob_sq = np.sum(A * A)

    assert dc == pytest.approx(frob_sq, rel=1e-6)

def test_rotation_preserves_invariants(tensor_module):
    A = symmetric_tensor()
    T = tensor_module.Tensor3x3(A.flatten().tolist())

    Q, _ = np.linalg.qr(np.random.randn(3, 3))
    A_rot = Q @ A @ Q.T
    T_rot = tensor_module.Tensor3x3(A_rot.flatten().tolist())

    assert T.trace() == pytest.approx(T_rot.trace())
    assert T.determinant() == pytest.approx(T_rot.determinant(), rel=1e-6)

def test_I1_invariant(tensor_module):
    A = random_tensor()
    T = tensor_module.Tensor3x3(A.flatten().tolist())

    Q, _ = np.linalg.qr(np.random.randn(3, 3))
    A_rot = Q @ A @ Q.T
    T_rot = tensor_module.Tensor3x3(A_rot.flatten().tolist())

    assert T.trace() == pytest.approx(T_rot.trace())


def test_J2_positive(tensor_module):
    A = random_tensor()
    T = tensor_module.Tensor3x3(A.flatten().tolist())

    assert T.J2() >= 0.0


def test_hydrostatic_deviatoric_zero(tensor_module):
    p = 5.0
    A = p * np.eye(3)
    T = tensor_module.Tensor3x3(A.flatten().tolist())

    dev = T.deviatoric()
    assert dev.doubleContraction(dev) == pytest.approx(0.0)


def test_near_singular(tensor_module):
    A = np.eye(3)
    A[2, 2] = 1e-12
    T = tensor_module.Tensor3x3(A.flatten().tolist())

    det_np = np.linalg.det(A)
    assert T.determinant() == pytest.approx(det_np, rel=1e-6)


def test_large_scale(tensor_module):
    A = random_tensor(scale=1e8)
    T = tensor_module.Tensor3x3(A.flatten().tolist())
    # to_tensor_cpp
    assert np.isfinite(T.trace())
    assert np.isfinite(T.determinant())


def test_small_scale(tensor_module):
    A = random_tensor(scale=1e-12)
    T = tensor_module.Tensor3x3(A.flatten().tolist())

    assert np.isfinite(T.trace())
    assert np.isfinite(T.determinant())
