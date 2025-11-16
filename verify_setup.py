#!/usr/bin/env python3
"""
Brilink Backend Setup Verification Script
Run this after setup to verify everything is working correctly.
"""

import sys
import os
import requests
import json
from datetime import datetime

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    required_packages = [
        'flask', 'sqlalchemy', 'flask_sqlalchemy',
        'pymysql', 'python_dotenv', 'jwt', 'werkzeug'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('_', ''))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False

    print("\n✅ All dependencies installed!")
    return True

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\n🔧 Checking environment configuration...")
    env_path = os.path.join(os.getcwd(), '.env')

    if not os.path.exists(env_path):
        print("❌ .env file not found!")
        print("Copy .env.example to .env and configure your database settings")
        return False

    # Check required environment variables
    required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'SECRET_KEY']
    missing_vars = []

    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)

        for var in required_vars:
            value = os.getenv(var)
            if not value or value.strip() == '':
                missing_vars.append(var)
            else:
                print(f"✅ {var} configured")
    except ImportError:
        print("⚠️  python-dotenv not available, skipping .env check")
        return True

    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please configure these in your .env file")
        return False

    print("\n✅ Environment configuration OK!")
    return True

def check_database_connection():
    """Test database connection"""
    print("\n🗄️  Checking database connection...")

    try:
        from dotenv import load_dotenv
        load_dotenv()

        import pymysql
        from config import config

        # Get database config
        db_config = config.get('development', {})
        if not db_config:
            print("❌ Database configuration not found!")
            return False

        # Test connection
        connection = pymysql.connect(
            host=db_config.get('DB_HOST', 'localhost'),
            user=db_config.get('DB_USER', 'root'),
            password=db_config.get('DB_PASSWORD', ''),
            database=db_config.get('DB_NAME', 'db_api_brilink'),
            port=int(db_config.get('DB_PORT', 3306))
        )

        connection.close()
        print("✅ Database connection successful!")
        return True

    except ImportError:
        print("⚠️  pymysql not available, skipping database check")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        print("Please check your database configuration in .env")
        return False

def check_api_health():
    """Test API health endpoint"""
    print("\n🌐 Checking API health...")

    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ API is healthy!")
                return True
            else:
                print("❌ API returned error response")
                return False
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        print("Make sure Flask app is running: python app.py")
        return False
    except Exception as e:
        print(f"❌ API health check failed: {str(e)}")
        return False

def main():
    """Main verification function"""
    print("=" * 50)
    print("🔍 Brilink Backend Setup Verification")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Directory: {os.getcwd()}")
    print()

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment Config", check_env_file),
        ("Database Connection", check_database_connection),
        ("API Health", check_api_health),
    ]

    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} check failed with error: {str(e)}")
            results.append((check_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)

    all_passed = True
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
        if not result:
            all_passed = False

    print()

    if all_passed:
        print("🎉 All checks passed! Your Brilink backend is ready!")
        print("\nNext steps:")
        print("1. Run database seeder: python seeder.py")
        print("2. Test API endpoints with Postman")
        print("3. Start developing your Flutter app!")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Install missing dependencies: pip install -r requirements.txt")
        print("- Configure .env file with correct database settings")
        print("- Start MySQL server")
        print("- Run Flask app: python app.py")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())