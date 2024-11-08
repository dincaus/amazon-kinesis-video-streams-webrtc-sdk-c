#!/bin/bash

# Navigate to the root directory of the project
cd "$(dirname "$0")/.." || exit

# Create the build directory if it doesn't exist
if [ ! -d "build" ]; then
    mkdir build
    echo "Created 'build' directory."
else
    echo "'build' directory already exists."
fi

# Navigate to the build directory
cd build || exit

# Run cmake command
echo "Running cmake .."
cmake ..

# Run make to build the project
echo "Running make"
make

echo "Build and compilation complete."