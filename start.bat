@echo off

set VENV=venv\Scripts

if EXIST %VENV% (
    echo Press Ctrl-C to stop
    %VENV%\python.exe -m dm_assist
) else (
    echo No Virtualenv exists.  Create one in 'venv' then run 'install.bat'
    echo Use the command 'python virtualenv venv' to create a virtual environment
    echo virtualenv can be installed with 'python -m pip install virtualenv' if needed
    exit 1
)