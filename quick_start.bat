@echo off
echo ========================================
echo Bionic Hand System - Quick Start
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Step 3: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Step 4: Running migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo IMPORTANT: Before running the server:
echo 1. Add your serviceAccountKey.json to project root
echo 2. Create .env file from .env.example
echo 3. Configure Firebase settings in .env
echo 4. Create superuser: python manage.py createsuperuser
echo.
echo To start the server: python manage.py runserver
echo.
pause
