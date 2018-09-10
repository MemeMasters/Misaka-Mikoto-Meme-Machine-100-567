@echo off

set VENV=venv\Scripts

if EXIST %VENV% (
    %VENV%\python.exe -m pip install -e .
) else (
    echo No Virtualenv exists.  Create one in 'venv'
    echo Use the command 'python virtualenv venv' to create a virtual environment
    echo virtualenv can be installed with 'python -m pip install virtualenv' if needed
    exit 1
)

echo You can now start the bot with '.\%VENV%\python.exe dm_assist' or start.bat