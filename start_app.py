#!/usr/bin/env python3
"""
Quick start script for the Lung Disease Classification web application.
Automatically detects available dependencies and runs the appropriate version.
"""

import sys
import os
import subprocess

def check_dependency(module_name):
    """Check if a Python module is available"""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def main():
    print("🫁 Lung Disease Classification Web Application")
    print("=" * 60)
    
    # Check which version to run
    has_flask = check_dependency('flask')
    has_tensorflow = check_dependency('tensorflow')
    
    print(f"Flask available: {'✅' if has_flask else '❌'}")
    print(f"TensorFlow available: {'✅' if has_tensorflow else '❌'}")
    print()
    
    if has_flask and has_tensorflow:
        print("🚀 Starting full application with TensorFlow model...")
        print("📍 URL: http://localhost:5000")
        print("⚠️  Note: Model needs to be trained for accurate predictions")
        print()
        
        try:
            from app import app
            app.run(debug=True, host='0.0.0.0', port=5000)
        except Exception as e:
            print(f"❌ Error starting full app: {e}")
            print("Falling back to simple version...")
            run_simple_app()
    
    elif has_flask:
        print("🚀 Starting Flask version without TensorFlow...")
        print("📍 URL: http://localhost:5000")
        print("⚠️  Note: Using mock predictions for demonstration")
        print()
        
        try:
            # Create a simple Flask version
            from flask import Flask, request, render_template, jsonify
            from simple_model import load_simple_model, predict_image_simple
            
            app = Flask(__name__)
            model = load_simple_model()
            
            @app.route('/')
            def index():
                return render_template('index.html')
            
            app.run(debug=True, host='0.0.0.0', port=5000)
        except Exception as e:
            print(f"❌ Error starting Flask app: {e}")
            print("Falling back to simple version...")
            run_simple_app()
    
    else:
        print("🚀 Starting simple HTTP server (no external dependencies)...")
        run_simple_app()

def run_simple_app():
    """Run the simple HTTP server version"""
    print("📍 URL: http://localhost:5000")
    print("⚠️  Note: Using mock predictions for demonstration")
    print("🔄 Press Ctrl+C to stop")
    print()
    
    try:
        from simple_app import run_server
        run_server(5000)
    except Exception as e:
        print(f"❌ Error starting simple app: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())