@echo off
echo ========================================
echo Check Build Requirements
echo ========================================
echo.

REM Activate virtual environment if exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo.
python check_requirements.py

pause
