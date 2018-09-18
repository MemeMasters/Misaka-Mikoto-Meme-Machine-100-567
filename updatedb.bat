@echo off

set VENV=..\..\venv\Scripts

if "%~1"=="" (
    echo Briefly describe the changes you have made:
    set /P message=
) else (
    set message=%1
)

echo %message%

cd dm_assist/sql

if EXIST %VENV% (
    %VENV%\activate.bat
    alembic revision --autogenerate -m "%message%"
) else (
    echo No Virtualenv exists.  Create one in 'venv' then run 'install.bat'
    echo Use the command 'python virtualenv venv' to create a virtual environment
    echo virtualenv can be installed with 'python -m pip install virtualenv' if needed
    exit 1
)

pause