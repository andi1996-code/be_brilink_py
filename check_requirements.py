"""
Check jika semua dependencies sudah terinstall dengan benar
"""
import sys

def check_dependencies():
    """Check if all required dependencies are installed"""
    
    required_packages = {
        'flask': 'Flask',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'sqlalchemy': 'SQLAlchemy',
        'dotenv': 'python-dotenv',
        'pymysql': 'pymysql',
        'werkzeug': 'Werkzeug',
        'jwt': 'PyJWT',
        'reportlab': 'reportlab',
        'PIL': 'Pillow',
        'tkinter': 'tkinter (built-in)',
        'PyInstaller': 'pyinstaller'
    }
    
    print("=" * 60)
    print("Checking Dependencies")
    print("=" * 60)
    print()
    
    missing = []
    installed = []
    
    for module, package in required_packages.items():
        try:
            if module == 'tkinter':
                import tkinter
                print(f"✓ {package:30} - OK")
                installed.append(package)
            else:
                __import__(module)
                print(f"✓ {package:30} - OK")
                installed.append(package)
        except ImportError:
            print(f"✗ {package:30} - MISSING")
            missing.append(package)
    
    print()
    print("=" * 60)
    print(f"Summary: {len(installed)}/{len(required_packages)} packages installed")
    print("=" * 60)
    
    if missing:
        print("\n❌ Missing packages:")
        for pkg in missing:
            print(f"   - {pkg}")
        
        print("\n📦 To install missing packages, run:")
        print("   pip install -r requirements.txt")
        
        if 'tkinter (built-in)' in missing:
            print("\n⚠ Note: tkinter should come with Python installation")
            print("   If missing, reinstall Python with tkinter support")
        
        return False
    else:
        print("\n✅ All dependencies are installed!")
        print("\n🎯 You can proceed with:")
        print("   1. Test GUI:        python database_config_gui.py")
        print("   2. Test Launcher:   python launcher.py")
        print("   3. Build EXE:       python build_exe.py")
        return True


def check_python_version():
    """Check if Python version is compatible"""
    print("\n" + "=" * 60)
    print("Checking Python Version")
    print("=" * 60)
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"\nPython Version: {version_str}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Your version: {version_str}")
        return False
    else:
        print("✅ Python version is compatible")
        return True


def check_files():
    """Check if all required files exist"""
    import os
    
    print("\n" + "=" * 60)
    print("Checking Required Files")
    print("=" * 60)
    print()
    
    required_files = [
        'launcher.py',
        'database_config_gui.py',
        'launcher.spec',
        'build_exe.py',
        'app.py',
        'config.py',
        'requirements.txt',
    ]
    
    required_dirs = [
        'models',
        'routes',
        'utils',
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            missing_files.append(file)
    
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"✓ {dir_name}/")
        else:
            print(f"✗ {dir_name}/ - MISSING")
            missing_dirs.append(dir_name)
    
    if missing_files or missing_dirs:
        print(f"\n❌ Missing {len(missing_files) + len(missing_dirs)} items")
        return False
    else:
        print("\n✅ All required files and directories present")
        return True


def main():
    """Main check process"""
    print("""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║     🔍 Brilink Backend - Pre-Build Check                   ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # Run all checks
    py_ok = check_python_version()
    files_ok = check_files()
    deps_ok = check_dependencies()
    
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    
    if py_ok and files_ok and deps_ok:
        print("\n🎉 All checks passed!")
        print("\n✅ System is ready for building executable")
        print("\nNext steps:")
        print("   1. Run: python build_exe.py")
        print("   2. Or:  build_exe.bat")
        return True
    else:
        print("\n❌ Some checks failed!")
        print("\nPlease fix the issues above before building.")
        return False


if __name__ == "__main__":
    try:
        success = main()
        print("\n" + "=" * 60)
        input("Press Enter to exit...")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error during check: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
