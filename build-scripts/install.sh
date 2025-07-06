#!/bin/sh

# This runs the install phase of the build.
#
# To run outside CodeBuild, set the following variables before running:
# GITHUB_WORKSPACE
#   Set this to your project's root directory.

install_dependencies() {
  echo "Installing Python lambda code dependencies"
  for function_directory in ${GITHUB_WORKSPACE}/src/* ; do
    cd ${function_directory}
    if [ -f "requirements.txt" ]; then
      echo "  Installing dependencies for ${function_directory}"
      pip install -r requirements.txt
    fi
    if [ -f "package.json" ]; then
      echo "  Installing dependencies for ${function_directory}"
      npm install
    fi
  done
}

install_python_layer_deps() {
  echo "Installing python deps"
  if [ -d "${GITHUB_WORKSPACE}/lambda/dependencies/python" ]; then
    cd ${GITHUB_WORKSPACE}/lambda/dependencies/python
    pip install -r requirements.txt -t .
  else
    echo "No python layer dependencies directory found, skipping"
  fi
}

echo "Starting install - $(date)"
STARTING_DIR=$PWD
set -xe

install_dependencies
install_python_layer_deps

cd $STARTING_DIR
unset STARTING_DIR
echo "Completed install - $(date)" 