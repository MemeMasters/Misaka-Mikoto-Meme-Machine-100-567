#!/bin/bash

WINDOWS_VENV="../../venv/Scripts"
UNIX_VENV="../../venv/bin"

if [ $# -eq 0 ]; then
    echo "briefly describe the changes you have made"
    read message
else
    message=$1
fi

cd dm_assist/sql

# Check if a virtualenv exists in a windows format
if [ -e $WINDOWS_VENV ]; then
    source "$WINDOWS_VENV/activate"
    alembic revision --autogenerate -m "$message"

# Check if a virtualenv exists in a unix format
elif [ -e $UNIX_VENV ]; then
    source "$UNIX_VENV/activate"
    alembic revision --autogenerate -m "$message"
else
    echo "No Virtualenv exists.  Create one in 'venv' then run 'install.sh'"
    echo "Use the command 'python virtualenv venv' to create a virtual environment"
    echo "virtualenv can be installed with 'python -m pip install virtualenv' if needed"
    exit 1
fi