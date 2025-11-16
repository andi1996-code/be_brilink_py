"""
Script untuk build executable menggunakan PyInstaller
"""
import os
import sys
import shutil
from pathlib import Path
import subprocess


def clean_build_folders():
    """Clean previous build folders"""
    print("🧹 Cleaning previous build folders...")
    folders_to_clean = ['build', 'dist', '__pycache__']
    
    for folder in folders_to_clean:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"  ✓ Removed {folder}")
            except Exception as e:
                print(f"  ⚠ Could not remove {folder}: {e}")
    
    # Remove spec files if not launcher.spec
    for spec_file in Path('.').glob('*.spec'):
        if spec_file.name != 'launcher.spec':
            try:
                spec_file.unlink()
                print(f"  ✓ Removed {spec_file}")
            except Exception as e:
                print(f"  ⚠ Could not remove {spec_file}: {e}")


def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print(f"✓ PyInstaller found (version {PyInstaller.__version__})")
        return True
    except ImportError:
        print("❌ PyInstaller not found!")
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to install PyInstaller: {e}")
            return False


def build_executable():
    """Build the executable using PyInstaller"""
    print("\n📦 Building executable...")
    print("=" * 60)
    
    # Build command
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "launcher.spec"
    ]
    
    print(f"Running: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        
        if result.returncode == 0:
            print("\n" + "=" * 60)
            print("✅ Build completed successfully!")
            print("=" * 60)
            
            exe_path = Path("dist") / "BrilinkBackend.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"\n📁 Executable created:")
                print(f"   Location: {exe_path.absolute()}")
                print(f"   Size: {size_mb:.2f} MB")
                
                # Create README in dist folder
                create_dist_readme()
                
                print("\n📋 Next steps:")
                print("   1. Navigate to the 'dist' folder")
                print("   2. Run BrilinkBackend.exe")
                print("   3. Configure your database connection")
                print("   4. Start the server")
                
                return True
        
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        return False


def create_dist_readme():
    """Create README in dist folder"""
    readme_content = """# Brilink Backend API - Executable

## How to Use

1. **Run the Application**
   - Double-click `BrilinkBackend.exe`
   - Or run from command prompt: `BrilinkBackend.exe`

2. **First Time Setup**
   - A configuration window will appear
   - Enter your MySQL database details:
     * Host (e.g., localhost)
     * Port (default: 3306)
     * Database Name (e.g., db_api_brilink)
     * Username
     * Password
     * Secret Key (for JWT tokens)

3. **Test Connection**
   - Click "Test Connection" to verify database settings
   - If successful, "Save & Start Server" button will be enabled

4. **Start Server**
   - Click "Save & Start Server"
   - The API server will start on http://localhost:5000

5. **Access the API**
   - Health Check: http://localhost:5000/health
   - See Postman collection for all available endpoints

## Requirements

- MySQL Server must be running
- Network access to MySQL server
- Required database user permissions

## Troubleshooting

### Connection Failed
- Check if MySQL server is running
- Verify username and password
- Check firewall settings
- Ensure database user has proper permissions

### Server Won't Start
- Check if port 5000 is already in use
- Verify .env file was created correctly
- Check database configuration

## Configuration File

The application creates a `.env` file in the same directory as the executable.
You can edit this file manually if needed:

```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=db_api_brilink
DB_USER=root
DB_PASSWORD=yourpassword
SECRET_KEY=your-secret-key
FLASK_ENV=production
```

## Support

For issues or questions, please contact the development team.

---
Built with ❤️ for Brilink
"""
    
    dist_path = Path("dist")
    if dist_path.exists():
        readme_path = dist_path / "README.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"   ✓ Created {readme_path}")


def main():
    """Main build process"""
    print("""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║           🏗️  Brilink Backend - Build Tool                 ║
║                                                            ║
║           Creating Windows Executable                      ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # Check PyInstaller
    if not check_pyinstaller():
        print("\n❌ Cannot proceed without PyInstaller")
        input("Press Enter to exit...")
        return
    
    # Clean previous builds
    clean_build_folders()
    
    # Build executable
    success = build_executable()
    
    if success:
        print("\n🎉 Build process completed successfully!")
    else:
        print("\n❌ Build process failed!")
    
    print("\n" + "=" * 60)
    input("Press Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Build cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
