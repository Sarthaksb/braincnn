@echo off
echo ====================================================
echo Starting Brain Tumor Classification Training...
echo ====================================================

set VENV_PY=%~dp0Brain-Tumar-classificaltion-using-CNN-main\.venv\Scripts\python.exe

if not exist "%VENV_PY%" (
    echo Virtual environment not found at %VENV_PY%
    pause
    exit /b 1
)

"%VENV_PY%" "%~dp0train.py" %*
pause

