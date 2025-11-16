@echo off
chcp 65001 >nul
title Brilink Backend - Master Menu
color 0A

:MENU
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║           🏦 BRILINK BACKEND API v2.0                      ║
echo ║                                                            ║
echo ║           Master Control Menu                              ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo.
echo  📋 MENU UTAMA
echo  ═══════════════════════════════════════════════════════════
echo.
echo   [1] 🔍 Check Requirements         - Cek dependencies
echo   [2] 🧪 Test Database Config GUI   - Test GUI konfigurasi
echo   [3] 🚀 Run Launcher               - Run aplikasi (dev mode)
echo   [4] 📦 Build EXE                  - Build executable
echo   [5] ⚡ Run EXE                    - Jalankan hasil build
echo.
echo   [6] 🌱 Run Seeder                 - Isi data awal database
echo   [7] 🔧 Install Dependencies       - Install semua packages
echo   [8] 🧹 Clean Build Files          - Hapus build cache
echo.
echo   [9] 📚 Open Documentation         - Buka panduan
echo   [0] ❌ Exit
echo.
echo  ═══════════════════════════════════════════════════════════
echo.

set /p choice="  Pilih menu (0-9): "

if "%choice%"=="1" goto CHECK_REQ
if "%choice%"=="2" goto TEST_GUI
if "%choice%"=="3" goto RUN_LAUNCHER
if "%choice%"=="4" goto BUILD_EXE
if "%choice%"=="5" goto RUN_EXE
if "%choice%"=="6" goto RUN_SEEDER
if "%choice%"=="7" goto INSTALL_DEPS
if "%choice%"=="8" goto CLEAN_BUILD
if "%choice%"=="9" goto OPEN_DOCS
if "%choice%"=="0" goto EXIT

echo.
echo  ❌ Pilihan tidak valid!
timeout /t 2 >nul
goto MENU

:CHECK_REQ
cls
echo.
echo  🔍 Checking Requirements...
echo  ══════════════════════════════════════════════════════════
echo.
call check_requirements.bat
goto MENU

:TEST_GUI
cls
echo.
echo  🧪 Testing Database Config GUI...
echo  ══════════════════════════════════════════════════════════
echo.
call test_gui.bat
goto MENU

:RUN_LAUNCHER
cls
echo.
echo  🚀 Running Launcher (Development Mode)...
echo  ══════════════════════════════════════════════════════════
echo.
call run_launcher.bat
goto MENU

:BUILD_EXE
cls
echo.
echo  📦 Building Executable...
echo  ══════════════════════════════════════════════════════════
echo.
call build_exe.bat
goto MENU

:RUN_EXE
cls
echo.
echo  ⚡ Running Executable...
echo  ══════════════════════════════════════════════════════════
echo.
if exist "dist\BrilinkBackend.exe" (
    cd dist
    BrilinkBackend.exe
    cd ..
) else (
    echo.
    echo  ❌ File BrilinkBackend.exe tidak ditemukan!
    echo  💡 Silakan build terlebih dahulu (Menu 4)
    echo.
    pause
)
goto MENU

:RUN_SEEDER
cls
echo.
echo  🌱 Running Database Seeder...
echo  ══════════════════════════════════════════════════════════
echo.
call run_seeder.bat
goto MENU

:INSTALL_DEPS
cls
echo.
echo  🔧 Installing Dependencies...
echo  ══════════════════════════════════════════════════════════
echo.

if exist venv\Scripts\activate.bat (
    echo  📦 Virtual environment ditemukan, mengaktifkan...
    call venv\Scripts\activate.bat
) else (
    echo  ⚠️  Virtual environment tidak ditemukan
    echo  💡 Membuat virtual environment baru...
    python -m venv venv
    if errorlevel 1 (
        echo  ❌ Gagal membuat virtual environment
        pause
        goto MENU
    )
    call venv\Scripts\activate.bat
)

echo.
echo  📥 Installing packages dari requirements.txt...
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo  ❌ Terjadi error saat instalasi!
    pause
) else (
    echo.
    echo  ✅ Semua dependencies berhasil diinstall!
    echo.
    pause
)
goto MENU

:CLEAN_BUILD
cls
echo.
echo  🧹 Cleaning Build Files...
echo  ══════════════════════════════════════════════════════════
echo.

if exist build (
    echo  🗑️  Menghapus folder build...
    rmdir /s /q build
)

if exist dist (
    echo  🗑️  Menghapus folder dist...
    rmdir /s /q dist
)

if exist __pycache__ (
    echo  🗑️  Menghapus folder __pycache__...
    rmdir /s /q __pycache__
)

for /d /r %%d in (__pycache__) do @if exist "%%d" (
    echo  🗑️  Menghapus %%d...
    rmdir /s /q "%%d"
)

for %%f in (*.pyc) do (
    echo  🗑️  Menghapus %%f...
    del /q "%%f"
)

echo.
echo  ✅ Build files berhasil dibersihkan!
echo.
pause
goto MENU

:OPEN_DOCS
cls
echo.
echo  📚 Opening Documentation...
echo  ══════════════════════════════════════════════════════════
echo.
echo  Dokumentasi tersedia:
echo.
echo   1. README_EXE.md       - Dokumentasi utama
echo   2. QUICKSTART.md       - Panduan cepat
echo   3. BUILD_GUIDE.md      - Panduan build detail
echo   4. README_SEEDER.md    - Panduan seeder
echo.
echo  Pilih file untuk dibuka (1-4) atau 0 untuk kembali:
echo.
set /p doc_choice="  Pilih: "

if "%doc_choice%"=="1" start README_EXE.md
if "%doc_choice%"=="2" start QUICKSTART.md
if "%doc_choice%"=="3" start BUILD_GUIDE.md
if "%doc_choice%"=="4" start README_SEEDER.md
if "%doc_choice%"=="0" goto MENU

timeout /t 1 >nul
goto MENU

:EXIT
cls
echo.
echo  ══════════════════════════════════════════════════════════
echo.
echo   👋 Terima kasih telah menggunakan Brilink Backend!
echo.
echo  ══════════════════════════════════════════════════════════
echo.
timeout /t 2 >nul
exit

:ERROR
echo.
echo  ❌ Terjadi kesalahan!
pause
goto MENU
