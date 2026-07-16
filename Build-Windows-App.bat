@echo off
REM ============================================================
REM   Python Pals - One-click Windows app builder
REM   Double-click this file. It installs everything it needs
REM   and produces a standalone app (no Python required to run).
REM ============================================================
setlocal
cd /d "%~dp0"
echo.
echo   ===============================================
echo     Building Python Pals for Windows...
echo   ===============================================
echo.

REM --- 1. Make sure Python is available -----------------------
where python >nul 2>nul
if errorlevel 1 (
    echo   [!] Python was not found on this PC.
    echo       Please install Python 3 from https://www.python.org/downloads/
    echo       During install, TICK the box "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

REM --- 2. Install the packaging tool (PyInstaller) -------------
echo   [1/2] Installing the app-builder (PyInstaller)...
python -m pip install --upgrade pip >nul
python -m pip install --upgrade pyinstaller
if errorlevel 1 (
    echo   [!] Could not install PyInstaller. Check your internet connection.
    pause
    exit /b 1
)

REM --- 3. Build the standalone .exe ---------------------------
echo.
echo   [2/2] Building the app (this can take a minute)...
python -m PyInstaller --noconfirm --windowed --onefile ^
    --name "Python Pals" --icon app_icon.ico ^
    --add-data "app_icon.ico;." app.py
if errorlevel 1 (
    echo   [!] Build failed. See messages above.
    pause
    exit /b 1
)

echo.
echo   ===============================================
echo     DONE!  Your app is here:
echo       dist\Python Pals.exe
echo.
echo     Double-click it to play. You can copy that one
echo     file to any Windows 10/11 PC - no Python needed.
echo   ===============================================
echo.
start "" "dist"
pause
