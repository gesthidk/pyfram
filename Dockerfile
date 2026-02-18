# Use official Python image as base
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        git \
        wget \
        curl \
        libeigen3-dev && \
    rm -rf /var/lib/apt/lists/*
   

# Install CMake 3.25 (you can change this easily!)
RUN wget https://github.com/Kitware/CMake/releases/download/v3.25.0/cmake-3.25.0-linux-x86_64.tar.gz && \
    tar -xzf cmake-3.25.0-linux-x86_64.tar.gz && \
    mv cmake-3.25.0-linux-x86_64 /opt/cmake && \
    ln -s /opt/cmake/bin/cmake /usr/local/bin/cmake && \
    rm cmake-3.25.0-linux-x86_64.tar.gz

# Verify CMake installation
RUN cmake --version

# Set working directory
WORKDIR /pyfram

# Copy project files
COPY . /pyfram/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


ENV PYTHONPATH=/pyfram/build

# Run tests by default
CMD ["pytest", "tests/", "-v"]
