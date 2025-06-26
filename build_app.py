#!/usr/bin/env python3
"""
Build script for SAST Aviator Desktop Application
This script properly packages the Flet app to avoid multiple window issues
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_directories():
    """Clean previous build artifacts"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}")
    
    # Clean .spec files
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"Removed {spec_file}")

def create_spec_file():
    """Create a custom spec file for PyInstaller"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('services', 'services'),
        ('ui', 'ui'),
        ('utils', 'utils'),
    ],
    hiddenimports=[
        'flet',
        'flet.core',
        'flet.utils',
        'configparser',
        'threading',
        'pathlib',
        'json',
        'logging',
        'logging.handlers',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SAST_Aviator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for windowed mode
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
    onefile=True,
)
'''
    
    with open('sast_aviator.spec', 'w') as f:
        f.write(spec_content)
    print("Created custom spec file")

def build_with_flet():
    """Build using Flet's pack command"""
    print("\n=== Building with Flet Pack ===")
    
    # Create a proper package.json for Flet
    package_info = {
        "name": "SAST Aviator",
        "version": "1.0.0",
        "description": "SAST Aviator Desktop Application"
    }
    
    # Build command
    cmd = [
        sys.executable, "-m", "flet", "pack",
        "main.py",
        "--name", "SAST_Aviator",
        "--icon", "assets/icon.ico" if os.path.exists("assets/icon.ico") else None,
        "--product-name", "SAST Aviator",
        "--product-version", "1.0.0",
        "--file-description", "SAST Aviator Desktop Application",
        "--copyright", "Copyright (c) 2025 OpenText",
        "--onefile",
        "--distpath", "dist",
    ]
    
    # Remove None values from cmd
    cmd = [arg for arg in cmd if arg is not None]
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ Flet build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Flet build failed: {e}")
        return False

def build_with_pyinstaller():
    """Build using PyInstaller with custom spec"""
    print("\n=== Building with PyInstaller ===")
    
    # Create spec file
    create_spec_file()
    
    # Build command
    cmd = [sys.executable, "-m", "PyInstaller", "sast_aviator.spec", "--clean"]
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ PyInstaller build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ PyInstaller build failed: {e}")
        return False

def create_build_info():
    """Create build information file"""
    import datetime
    
    build_info = f"""SAST Aviator Desktop Application
Build Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Platform: {sys.platform}
Python Version: {sys.version}

To run the application:
- Windows: Double-click SAST_Aviator.exe
- macOS: Double-click SAST_Aviator.app
- Linux: Run ./SAST_Aviator

Note: Ensure FCLI and OpenSSL are installed and available in PATH.
"""
    
    with open('dist/README.txt', 'w') as f:
        f.write(build_info)
    print("Created build info file")

def main():
    """Main build process"""
    print("SAST Aviator Build Script")
    print("=" * 50)
    
    # Clean previous builds
    clean_build_directories()
    
    # Create dist directory
    os.makedirs('dist', exist_ok=True)
    
    # Try Flet build first (recommended)
    success = build_with_flet()
    
    # If Flet fails, try PyInstaller
    if not success:
        print("\nFlet build failed, trying PyInstaller...")
        success = build_with_pyinstaller()
    
    if success:
        create_build_info()
        print("\n✓ Build completed successfully!")
        print(f"Executable location: {Path('dist').absolute()}")
        
        # Additional instructions for avoiding multiple windows
        print("\n" + "="*50)
        print("IMPORTANT: To avoid multiple window issues:")
        print("1. The application includes single-instance checking")
        print("2. If you see multiple windows, check Task Manager and end all instances")
        print("3. Always use the executable from the 'dist' folder")
        print("4. Do not run multiple build commands simultaneously")
    else:
        print("\n✗ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()