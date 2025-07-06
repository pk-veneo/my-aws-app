#!/bin/sh

# This runs the install phase of the build.
#
# To run outside CodeBuild, set the following variables before running:
# GITHUB_WORKSPACE
#   Set this to your project's root directory.

# copy_api_auth_template() {
#   echo "Copying Cirrus Authenticators template from S3"
#   aws s3 cp s3://lly-templates/aws-authenticators/cloudformation/prod.yaml ${GITHUB_WORKSPACE}/api-authenticators/authenticators.yaml
# }

install_dependencies() {
  echo "Installing Python lambda code dependencies"
  for function_directory in ${GITHUB_WORKSPACE}/lambda/* ; do
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
  echo "Installng python deps"
  cd ${GITHUB_WORKSPACE}/lambda/dependencies/python
  pip install -r requirements.txt -t .
}

echo "Starting install - $(date)"
STARTING_DIR=$PWD
set -xe

# copy_api_auth_template
install_dependencies
install_python_layer_deps

cd $STARTING_DIR
unset STARTING_DIR
echo "Completed install - $(date)"