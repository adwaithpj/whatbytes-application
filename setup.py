#!/usr/bin/env python3
"""
Healthcare Backend Setup Script
This script helps set up the development environment
"""

import os
import sys
import subprocess
from django.core.management.utils import get_random_secret_key

def create_env_file():
    """Create .env file with default values"""
    env_content = f"""# Database Configuration
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Django Configuration
SECRET_KEY={get_random_secret_key()}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with default configuration")
        print("⚠️  Please update the database password in .env file")
    else:
        print("ℹ️  .env file already exists")

def run_migrations():
    """Run Django migrations"""
    try:
        print("🔄 Making migrations...")
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        
        print("🔄 Applying migrations...")
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        
        print("✅ Migrations completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running migrations: {e}")
        return False
    return True

def create_superuser():
    """Prompt to create superuser"""
    response = input("Do you want to create a superuser? (y/n): ").lower()
    if response == 'y':
        try:
            subprocess.run([sys.executable, 'manage.py', 'createsuperuser'], check=True)
            print("✅ Superuser created successfully")
        except subprocess.CalledProcessError:
            print("❌ Error creating superuser")

def main():
    """Main setup function"""
    print("🏥 Healthcare Backend Setup")
    print("=" * 30)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Run migrations
    if run_migrations():
        # Create superuser
        create_superuser()
        
        print("\n🎉 Setup completed!")
        print("\nNext steps:")
        print("1. Update database credentials in .env file")
        print("2. Ensure PostgreSQL is running")
        print("3. Run: python manage.py runserver")
        print("4. Visit: http://localhost:8000/admin/ for admin interface")
        print("5. API endpoints available at: http://localhost:8000/api/")
    else:
        print("\n❌ Setup incomplete. Please fix the errors and try again.")

if __name__ == "__main__":
    main()