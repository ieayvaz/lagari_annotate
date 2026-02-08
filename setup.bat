@echo off
echo ======================================
echo UAV Annotation Tool - Quick Start
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo X pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo [OK] pip found

REM Create images folder if it doesn't exist
if not exist "images" (
    echo [*] Creating images folder...
    mkdir images
    echo [!] Please add your UAV images to the 'images' folder before starting the server.
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo [*] Installing dependencies...
pip install -r requirements.txt

echo.
echo [OK] Setup complete!
echo.
echo To start the server, run: start_server.bat
echo.
pause
