from app import create_app
import traceback
import sys
import os
from pathlib import Path

def check_env_file():
    """Check if .env file exists, if not run setup"""
    env_path = Path('.env')
    if not env_path.exists():
        print("Configuration file (.env) not found!")
        print("Running setup...\n")
        from setup_app import main as setup_main
        setup_main()

if __name__ == '__main__':
    try:
        # Check and setup configuration if needed
        check_env_file()
        
        app = create_app()
        print("\n✓ App created successfully")
        print("=" * 50)
        print("Server running on: http://0.0.0.0:5000")
        print("=" * 50 + "\n")
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"\n✗ Error starting app: {e}")
        traceback.print_exc()
        input("\nPress Enter to exit...")  # Keep console open
