@echo off
title AI Resume Analyzer
echo ============================================
echo   AI Resume Analyzer - One-Click Setup
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Install dependencies
echo [1/2] Installing dependencies...
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo [2/2] Starting server...
echo.
echo ============================================
echo   Open http://127.0.0.1:8000 in browser
echo   Press Ctrl+C to stop
echo ============================================
echo.

:: Open browser after a short delay
start "" cmd /c "timeout /t 3 /nobreak >nul & start http://127.0.0.1:8000"

:: Run the app
python app.py
pause
