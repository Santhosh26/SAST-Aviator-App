#!/usr/bin/env python3
"""
Setup script to create the project directory structure
Run this script to create all necessary directories for the SAST Aviator app
"""

import os
from pathlib import Path

def create_project_structure():
    """Create the project directory structure"""
    
    # Define the directory structure
    directories = [
        "sast_aviator_app",
        "sast_aviator_app/config",
        "sast_aviator_app/ui",
        "sast_aviator_app/ui/components",
        "sast_aviator_app/services",
        "sast_aviator_app/utils",
        "sast_aviator_app/assets"
    ]
    
    # Create directories
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")
    
    print("\nProject structure created successfully!")
    print("\nNext steps:")
    print("1. Copy all the Python files to their respective directories")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the application: python main.py")

if __name__ == "__main__":
    create_project_structure()