#!/bin/bash

echo "========================================"
echo "  Brilink Backend Setup Script (Linux/Mac)"
echo "========================================"
echo

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "Error: Please run this script from the backend_brilink_v2 directory!"
    exit 1
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed!"
    echo "Please install Python 3.8+ first."
    exit 1
fi

echo "Python found! Checking version..."
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment!"
        exit 1
    fi
    echo "Virtual environment created successfully!"
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment!"
    exit 1
fi

# Upgrade pip
echo
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo
echo "Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies!"
    echo "Please check your internet connection and try again."
    deactivate
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo
    echo "Creating .env file from template..."
    cp .env.example .env
    echo
    echo "IMPORTANT: Please edit .env file with your database credentials!"
    echo "File location: $(pwd)/.env"
    echo
    echo "You can edit it with: nano .env"
fi

# Deactivate virtual environment
deactivate

echo
echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo
echo "Next steps:"
echo "1. Edit .env file with your database credentials"
echo "2. Make sure MySQL is running"
echo "3. Run: python app.py"
echo "4. Test: curl http://localhost:5000/api/health"
echo
echo "For database seeding, run: python seeder.py"
echo