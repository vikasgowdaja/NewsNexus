@echo off
setlocal

set "ROOT=%~dp0"
set "PYTHON_EXE=%ROOT%.venv\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Missing .venv interpreter at "%PYTHON_EXE%"
    echo [ERROR] Create the virtual environment and install requirements first.
    exit /b 1
)

"%PYTHON_EXE%" "%ROOT%run_all.py" %*
exit /b %errorlevel%