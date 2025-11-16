@echo off
echo ========================================
echo Brilink Backend - Run Launcher
echo ========================================
echo.

REM Activate virtual environment if exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo.
echo Starting application...
python launcher.py

pause
