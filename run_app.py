#!/usr/bin/env python3
"""
Simple script to run the Lung Disease Classification web application
"""

import os
import sys

def main():
    print("=" * 60)
    print("Lung Disease Classification Web Application")
    print("=" * 60)
    
    # Check if required files exist
    required_files = ['app.py', 'model.py', 'templates/index.html']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return 1
    
    print("✅ All required files found")
    print("\n📋 Instructions:")
    print("1. Make sure you have installed the requirements: pip install -r requirements.txt")
    print("2. The application will start on http://localhost:5000")
    print("3. Upload X-ray images to get lung disease predictions")
    print("\n⚠️  Note: This model needs to be trained first for accurate predictions")
    print("   The current model uses random weights for demonstration purposes")
    
    print("\n🚀 Starting application...")
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"❌ Error importing Flask app: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())