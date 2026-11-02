#!/bin/bash



echo "  "
echo "The script you are running has:"
echo "basename: [$(basename "$0")]"
echo "dirname : [$(dirname "$0")]"
echo "pwd     : [$(pwd)]"

current_dir="$(pwd)"
echo   "current_dir:  $current_dir "

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Script directory: $SCRIPT_DIR"




echo    "PYTHON_VENV  : $PYTHON_VENV"
cd       $PYTHON_VENV

#source   py_13_qt5/bin/activate
source   py_13_qt6/bin/activate

cd       $SCRIPT_DIR

which    python

# Run the Python program

python     main.py

exec bash

# here just wait   ( or comment out )
#echo "enter to exit"
#read RESPONSE
