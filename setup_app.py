import os
import sys
from pathlib import Path

def get_db_config():
    """Get database configuration from user input"""
    print("=" * 50)
    print("Database Configuration Setup")
    print("=" * 50)
    
    db_host = input("Database Host [localhost]: ").strip() or "localhost"
    db_port = input("Database Port [3306]: ").strip() or "3306"
    db_user = input("Database User: ").strip()
    db_password = input("Database Password: ").strip()
    db_name = input("Database Name: ").strip()
    
    if not db_user or not db_password or not db_name:
        print("\nError: Database user, password, and name are required!")
        return None
    
    return {
        'DB_HOST': db_host,
        'DB_PORT': db_port,
        'DB_USER': db_user,
        'DB_PASSWORD': db_password,
        'DB_NAME': db_name,
        'DB_DRIVER': 'mysql+pymysql'
    }

def create_env_file(config):
    """Create .env file with database configuration"""
    env_path = Path('.env')
    
    env_content = f"""FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-change-this

DB_HOST={config['DB_HOST']}
DB_PORT={config['DB_PORT']}
DB_USER={config['DB_USER']}
DB_PASSWORD={config['DB_PASSWORD']}
DB_NAME={config['DB_NAME']}
"""
    
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        print(f"\n✓ .env file created successfully at: {env_path.absolute()}")
        return True
    except Exception as e:
        print(f"\n✗ Error creating .env file: {e}")
        return False

def test_database_connection(config):
    """Test database connection"""
    try:
        import pymysql
        
        print("\nTesting database connection...")
        connection = pymysql.connect(
            host=config['DB_HOST'],
            port=int(config['DB_PORT']),
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            database=config['DB_NAME']
        )
        connection.close()
        print("✓ Database connection successful!")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("Please check your database credentials and try again.")
        return False

def main():
    """Main setup function"""
    print("\n")
    print("╔════════════════════════════════════════╗")
    print("║   Backend Brilink - Setup Configuration   ║")
    print("╚════════════════════════════════════════╝\n")
    
    # Get database configuration from user
    config = get_db_config()
    if not config:
        sys.exit(1)
    
    # Create .env file
    if not create_env_file(config):
        sys.exit(1)
    
    # Test database connection
    if not test_database_connection(config):
        retry = input("\nDo you want to reconfigure? (yes/no): ").strip().lower()
        if retry == 'yes':
            main()
        else:
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("You can now run the application.")
    print("=" * 50 + "\n")

if __name__ == '__main__':
    main()
