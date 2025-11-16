"""
Main launcher untuk aplikasi backend Brilink
Menggabungkan GUI konfigurasi database dan server Flask
"""
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_database_connection():
    """Check if database is configured and accessible"""
    from dotenv import load_dotenv
    import pymysql
    
    load_dotenv()
    
    try:
        host = os.getenv('DB_HOST')
        port = int(os.getenv('DB_PORT', 3306))
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        dbname = os.getenv('DB_NAME')
        
        if not all([host, user, dbname]):
            return False, "Database configuration incomplete"
        
        # Test connection
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            connect_timeout=5
        )
        
        # Check/create database
        cursor = connection.cursor()
        cursor.execute(f"SHOW DATABASES LIKE '{dbname}'")
        db_exists = cursor.fetchone()
        
        if not db_exists:
            print(f"Creating database '{dbname}'...")
            cursor.execute(f"CREATE DATABASE `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✓ Database '{dbname}' created successfully")
        
        cursor.close()
        connection.close()
        
        return True, "Database connection successful"
        
    except Exception as e:
        return False, f"Database connection error: {str(e)}"


def run_configuration_gui():
    """Run the database configuration GUI"""
    from database_config_gui import main as run_gui
    return run_gui()


def start_flask_server():
    """Start the Flask server"""
    from app import create_app
    
    print("\n" + "="*60)
    print("🚀 Starting Brilink Backend API Server")
    print("="*60 + "\n")
    
    app = create_app('production')
    
    print("\n" + "="*60)
    print("✓ Server is running!")
    print("="*60)
    print(f"📡 API Base URL: http://localhost:5000")
    print(f"🏥 Health Check: http://localhost:5000/health")
    print(f"📚 API Documentation: Check Postman collection")
    print("="*60)
    print("\nPress CTRL+C to stop the server\n")
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("🛑 Server stopped by user")
        print("="*60)
    except Exception as e:
        print(f"\n❌ Server error: {str(e)}")
        input("\nPress Enter to exit...")


def main():
    """Main entry point"""
    print("""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║           🏦 BRILINK BACKEND API v2.0                      ║
║                                                            ║
║           Database Configuration & Server Launcher         ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # Check if .env exists and is valid
    env_file = Path('.env')
    need_config = True
    
    if env_file.exists():
        print("📋 Found existing configuration...")
        can_connect, message = check_database_connection()
        
        if can_connect:
            print(f"✓ {message}")
            print("\n1. Use existing configuration")
            print("2. Reconfigure database settings")
            
            choice = input("\nEnter your choice (1 or 2, default=1): ").strip() or "1"
            
            if choice == "1":
                need_config = False
                should_start = True
            else:
                need_config = True
        else:
            print(f"⚠ {message}")
            print("Configuration needed...")
            need_config = True
    else:
        print("📋 No configuration found. Setup required...")
    
    # Run configuration GUI if needed
    if need_config:
        print("\n🔧 Opening configuration window...\n")
        should_start = run_configuration_gui()
        
        if not should_start:
            print("\n❌ Configuration cancelled. Exiting...")
            return
        
        # Verify connection again after configuration
        can_connect, message = check_database_connection()
        if not can_connect:
            print(f"\n❌ {message}")
            input("\nPress Enter to exit...")
            return
    
    # Start Flask server
    try:
        start_flask_server()
    except Exception as e:
        print(f"\n❌ Failed to start server: {str(e)}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Critical error: {str(e)}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
