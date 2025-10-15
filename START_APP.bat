@echo off
setlocal enabledelayedexpansion

:: =============================================================================
:: Email Scraper Tool - Enterprise Launcher
:: Version: 2.0.0
:: =============================================================================

title Email Scraper Tool v2.0.0

:: Set console colors for professional appearance
color 0A

:: Clear screen and display header
cls
echo.
echo ================================================================================
echo                          EMAIL SCRAPER TOOL v2.0.0
echo ================================================================================
echo.
echo Starting Email Scraper Web Application...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Display Python version
echo [INFO] Python version:
python --version

:: Check if app.py exists
if not exist "app.py" (
    echo.
    echo [ERROR] app.py file not found in current directory
    echo Please ensure you are running this script from the correct location.
    echo.
    pause
    exit /b 1
)

:: Check if required Python packages are available
echo.
echo [INFO] Checking dependencies...
python -c "import flask, requests" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Required Python packages not found
    echo Please install required packages:
    echo    pip install flask requests
    echo.
    pause
    exit /b 1
)

echo [INFO] All dependencies verified
echo.

:: Display launch information
echo ================================================================================
echo                               LAUNCH SETTINGS
echo ================================================================================
echo Application URL: http://localhost:5000
echo Auto-browser: Enabled
echo Debug Mode: Disabled
echo Port: 5000
echo.
echo [INFO] Your default browser will open automatically
echo [INFO] Keep this window open while using the application
echo [INFO] Press Ctrl+C to stop the server when finished
echo ================================================================================
echo.

:: Wait a moment before starting
timeout /t 3 /nobreak >nul

:: Start the application with error handling
echo [INFO] Launching Email Scraper Tool...
echo.

python app.py
set exit_code=%errorlevel%

:: Handle exit codes
echo.
if %exit_code% equ 0 (
    echo [INFO] Application closed successfully
) else (
    echo [ERROR] Application exited with code %exit_code%
    echo This usually indicates an error occurred during execution
)

echo.
echo ================================================================================
echo                            SESSION COMPLETED
echo ================================================================================
echo.
pause
