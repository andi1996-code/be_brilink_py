@echo off
echo ========================================
echo Quick Fix - Install Pillow and Rebuild
echo ========================================
echo.

REM Activate virtual environment if exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo.
echo Installing missing dependency (Pillow)...
pip install Pillow

if errorlevel 1 (
    echo.
    echo ❌ Failed to install Pillow
    pause
    exit /b 1
)

echo.
echo ✅ Pillow installed successfully!
echo.
echo Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo Rebuilding executable...
python build_exe.py

echo.
echo ========================================
echo Done!
echo ========================================
pause
