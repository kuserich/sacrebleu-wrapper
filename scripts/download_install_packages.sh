#! /bin/bash

SCRIPTS_DIR=`dirname "$0"`
BASE_DIR=${SCRIPTS_DIR}/..

VENVS_DIR=${BASE_DIR}/venvs
APP_NAME="BLEUette"

python_location=`which python`

if [[ $python_location == *"/usr/bin"* ]]; then
    echo "Do not run this script without activating a virtual environment first"
    echo "To activate your virtual environment:"
    echo "source ${VENVS_DIR}/${APP_NAME}/bin/activate"
    exit
fi

pip install sacrebleu
pip install mosestokenizer
