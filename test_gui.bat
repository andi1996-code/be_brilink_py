@echo off
echo ========================================
echo Test Database Configuration GUI
echo ========================================
echo.

REM Activate virtual environment if exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo.
echo Running GUI test...
python database_config_gui.py

pause
