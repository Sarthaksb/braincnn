@echo off
cd /d "%~dp0"
echo ====================================================
echo Starting Brain Tumor Classification Web App...
echo ====================================================

set "VENV_DIR=%~dp0.venv\Scripts"
if not exist "%VENV_DIR%\python.exe" (
    set "VENV_DIR=%~dp0..\Brain-Tumar-classificaltion-using-CNN-main\.venv\Scripts"
)

if not exist "%VENV_DIR%\python.exe" (
    echo [ERROR] Could not find Python virtual environment.
    pause
    exit /b 1
)

echo Starting Streamlit app on http://localhost:8501 ...
echo.

"%VENV_DIR%\python.exe" -m streamlit run app.py

pause
