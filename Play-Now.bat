@echo off
REM Quick way to play right away using Python (no build needed).
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Install it from https://www.python.org/downloads/
    echo Remember to tick "Add Python to PATH" during install.
    pause
    exit /b 1
)
start "" pythonw app.py
