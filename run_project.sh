#!/bin/bash

# run_project.sh - Unified script to setup and run the DriveDeal Marketplace

echo "🚀 Starting DriveDeal Marketplace Setup & Run Script..."

# 1. Setup Virtual Environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# 2. Install/Update dependencies
echo "📥 Installing requirements..."
./venv/bin/pip install -r requirements.txt

# 3. Initialize Database
echo "🗄️ Initializing database..."
./venv/bin/python3 scripts/init_db.py

# 4. Populate Mock Data
echo "🚗 Populating mock data..."
./venv/bin/python3 scripts/populate_mock_data.py

# 5. Run Unit Tests for DAA Algorithms (Verification)
echo "🧪 Running DAA Algorithm Verification tests..."
./venv/bin/python3 backend/test_DAA.py

# 6. Run the Application
echo "🌐 Starting Flask Application..."
echo "Access the app at http://127.0.0.1:5000"
./venv/bin/python3 backend/app.py
