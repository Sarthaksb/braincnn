@echo off
cd /d "%~dp0"
echo ====================================================
echo Starting Brain Tumor Classification Web App...
echo ====================================================

set VENV_PY=""
if exist "%~dp0Brain-Tumar-classificaltion-using-CNN-main\.venv\Scripts\python.exe" (
    set VENV_PY="%~dp0Brain-Tumar-classificaltion-using-CNN-main\.venv\Scripts\python.exe"
) else if exist "%~dp0.venv\Scripts\python.exe" (
    set VENV_PY="%~dp0.venv\Scripts\python.exe"
) else if exist "%~dp0..\Brain-Tumar-classificaltion-using-CNN-main\.venv\Scripts\python.exe" (
    set VENV_PY="%~dp0..\Brain-Tumar-classificaltion-using-CNN-main\.venv\Scripts\python.exe"
)

if %VENV_PY%=="" (
    echo [ERROR] Virtual environment (.venv) not found!
    pause
    exit /b 1
)

set APP_PY="%~dp0app.py"
if not exist %APP_PY% (
    if exist "%~dp0..\app.py" (
        set APP_PY="%~dp0..\app.py"
    )
)

echo Using Python: %VENV_PY%
echo Launching Streamlit web application on http://localhost:8501 ...
echo.
%VENV_PY% -m streamlit run %APP_PY% --server.headless false

pause
