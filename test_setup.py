#!/usr/bin/env python3
"""
Test script to validate the project setup and VS Code configuration.

This script checks if all the necessary dependencies can be imported
and if the basic functionality works as expected.
"""

import sys
import os


def test_basic_imports():
    """Test basic Python imports that should be available."""
    print("Testing basic imports...")
    
    tests = [
        ("os", "Standard library - os module"),
        ("sys", "Standard library - sys module"),
        ("json", "Standard library - json module"),
    ]
    
    for module_name, description in tests:
        try:
            __import__(module_name)
            print(f"✓ {description}")
        except ImportError as e:
            print(f"✗ {description}: {e}")


def test_ml_imports():
    """Test machine learning library imports."""
    print("\nTesting ML library imports...")
    
    ml_tests = [
        ("numpy", "NumPy - numerical computing"),
        ("matplotlib.pyplot", "Matplotlib - plotting"),
        ("sklearn", "Scikit-learn - machine learning"),
        ("tensorflow", "TensorFlow - deep learning"),
        ("xgboost", "XGBoost - gradient boosting"),
        ("seaborn", "Seaborn - statistical visualization"),
        ("PIL", "Pillow - image processing"),
    ]
    
    for module_name, description in ml_tests:
        try:
            __import__(module_name)
            print(f"✓ {description}")
        except ImportError as e:
            print(f"✗ {description}: {e}")
            print(f"  To install: pip install {module_name}")


def test_project_structure():
    """Test if the project structure is correct."""
    print("\nTesting project structure...")
    
    expected_files = [
        "requirements.txt",
        "README.md",
        "Lung Diseases Classification.ipynb",
        "lung_diseases_classification.py",
        ".vscode/settings.json",
        ".vscode/extensions.json",
        ".vscode/launch.json",
        ".gitignore",
        "pyproject.toml",
        "setup.py"
    ]
    
    for file_path in expected_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - missing")


def test_vs_code_config():
    """Test VS Code configuration files."""
    print("\nTesting VS Code configuration...")
    
    import json
    
    config_files = {
        ".vscode/settings.json": "VS Code settings",
        ".vscode/extensions.json": "Recommended extensions",
        ".vscode/launch.json": "Debug configurations"
    }
    
    for file_path, description in config_files.items():
        try:
            with open(file_path, 'r') as f:
                config = json.load(f)
            print(f"✓ {description} - valid JSON")
            
            # Check specific settings
            if file_path == ".vscode/settings.json":
                if "python.defaultInterpreterPath" in config:
                    print("  ✓ Python interpreter path configured")
                if "jupyter.notebookFileRoot" in config:
                    print("  ✓ Jupyter notebook root configured")
                    
        except FileNotFoundError:
            print(f"✗ {description} - file not found")
        except json.JSONDecodeError as e:
            print(f"✗ {description} - invalid JSON: {e}")


def main():
    """Main test function."""
    print("=== VS Code Project Setup Test ===")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    test_basic_imports()
    test_ml_imports()
    test_project_structure()
    test_vs_code_config()
    
    print("\n=== Test Summary ===")
    print("If you see ✗ marks for ML libraries, run:")
    print("  pip install -r requirements.txt")
    print("\nFor development tools, also run:")
    print("  pip install -r dev-requirements.txt")
    print("\nThen restart VS Code to apply all configurations.")


if __name__ == "__main__":
    main()