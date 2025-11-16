#!/usr/bin/env python
"""
Debug script untuk test aplikasi
"""
import sys
import traceback
import os

print("=" * 60)
print("Backend Brilink - Debug Mode")
print("=" * 60)
print()

# Test 1: Check Python version
print("[1] Checking Python version...")
print(f"    Python {sys.version}")
print(f"    Executable: {sys.executable}")
print()

# Test 2: Check current directory
print("[2] Checking current directory...")
print(f"    Current: {os.getcwd()}")
print(f"    Files: {os.listdir('.')[:5]}")
print()

# Test 3: Check if .env exists
print("[3] Checking .env file...")
if os.path.exists('.env'):
    print("    ✓ .env file found")
else:
    print("    ✗ .env file NOT found")
print()

# Test 4: Import modules
print("[4] Importing modules...")
try:
    import flask
    print(f"    ✓ Flask {flask.__version__}")
except Exception as e:
    print(f"    ✗ Flask error: {e}")

try:
    import sqlalchemy
    print(f"    ✓ SQLAlchemy {sqlalchemy.__version__}")
except Exception as e:
    print(f"    ✗ SQLAlchemy error: {e}")

try:
    import pymysql
    print(f"    ✓ PyMySQL")
except Exception as e:
    print(f"    ✗ PyMySQL error: {e}")

try:
    import flask_sqlalchemy
    print(f"    ✓ Flask-SQLAlchemy")
except Exception as e:
    print(f"    ✗ Flask-SQLAlchemy error: {e}")
print()

# Test 5: Load config
print("[5] Loading configuration...")
try:
    from config import config
    print(f"    ✓ Config loaded")
    for env_name in config:
        print(f"      - {env_name}")
except Exception as e:
    print(f"    ✗ Config error: {e}")
    traceback.print_exc()
print()

# Test 6: Load models
print("[6] Loading models...")
try:
    from models.user import db
    print(f"    ✓ User model loaded")
except Exception as e:
    print(f"    ✗ User model error: {e}")
    traceback.print_exc()
print()

# Test 7: Create app
print("[7] Creating Flask app...")
try:
    from app import create_app
    app = create_app()
    print(f"    ✓ App created successfully")
    print(f"    App name: {app.name}")
    print(f"    Debug: {app.debug}")
except Exception as e:
    print(f"    ✗ App creation error: {e}")
    traceback.print_exc()
    print()
    print("ERROR DETAILS:")
    traceback.print_exc()
print()

print("=" * 60)
print("Debug test completed!")
print("=" * 60)
input("Press Enter to exit...")
