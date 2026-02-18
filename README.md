# pyfram

**pyfram** is a framework for developing and testing C++ modules with Python bindings using pybind11, fully containerized with Docker for a reproducible development environment.

## Features

-  **Flexible C++ Module Support**: Test any C++ module with Python bindings
-  **Python Bindings**: Automatic integration via [pybind11](https://pybind11.readthedocs.io/)
-  **Comprehensive Testing**: pytest-based test suite with NumPy integration
-  **Docker Support**: Reproducible builds and tests
-  **Extensible**: Add new C++ modules and tests

## Requirements 

- Docker
- Docker Compose

No local C++ or Python dependencies are required.
All build tools and libraries are installed inside the container.

### Run Tests

**First time or after code updates:**
```bash
docker compose up --build
```

**Clean up and rebuild:**
```bash
docker compose down
sudo rm -rf build/
docker compose up --build
```

## Project Structure

```
pyfram/
|── cpp_modules/          # C++ source code
|   |── tensor.h          # Example: Tensor3x3 class
|   |── tensor.cpp        # Example: Tensor3x3 implementation
|   |── tensor_py.cpp     # Example: Python bindings (pybind11)
|── tests/
|   |── test_tensor.py    # Example: Tensor tests
|── build/                # (Auto-generated) Build outputs
|── Dockerfile            # Docker configuration
|── docker-compose.yml    # Docker Compose setup
|── CMakeLists.txt        # Build configuration
|── requirements.txt      # Python dependencies
|── README.md             
|__ LICENSE 

```

## Adding a New C++ Module

Let's say you want to add a mesh module:

1. **Create C++ source files** in `cpp_modules/`:
   - `mesh.h` (header with `class Mesh`)
   - `mesh.cpp` (implementation)
   - `mesh_py.cpp` (pybind11 bindings)

2. **Update `CMakeLists.txt`** to add your new module:
   ```cmake
   pybind11_add_module(mesh_py
       cpp_modules/mesh_py.cpp
   )
   target_link_libraries(mesh_py PRIVATE tensor)
   ```

3. **Write Python tests** in `tests/`

4. **Run tests**


## Development Workflow

1. **Write C++ code** in `cpp_modules/`
2. **Create pybind11 bindings** in `*_py.cpp`
3. **Update CMakeLists.txt** to build your module
4. **Write Python tests** in `tests/`
5. **Run**: `docker compose up --build`
6. **Iterate and improve**

## License

```
MIT License
```

## Troubleshooting

### If permission denied on `rm -rf build/`
The `build/` folder might be owned by Docker. Use `sudo`:
```bash
sudo rm -rf build/
```
