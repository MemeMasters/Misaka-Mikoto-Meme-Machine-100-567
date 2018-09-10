#!/bin/bash

WINDOWS_VENV="venv/Scripts"
UNIX_VENV="venv/bin"


# Check if a virtualenv exists in a windows format
if [ -e $WINDOWS_VENV ]; then
    "$WINDOWS_VENV/python.exe" -m pip install -e .
    
    VENV=$WINDOWS_VENV
# Check if a virtualenv exists in a unix format
elif [ -e $UNIX_VENV ]; then
    "$UNIX_VENV/python" -m pip install -e .

    VENV=$UNIX_VENV
else
    echo "No Virtualenv exists.  Create one in 'venv'"
    echo "Use the command 'python virtualenv venv' to create a virtual environment"
    echo "virtualenv can be installed with 'python -m pip install virtualenv' if needed"
    exit 1
fi

echo "You can now start the bot with 'source $VENV/activate && dm_assist' or 'start.sh'."