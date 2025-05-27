#!/usr/bin/env python3
"""
Setup script for F1 Race Position Predictor
This script helps set up the project environment and dependencies
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major != 3 or version.minor < 8:
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version {version.major}.{version.minor} is compatible")
    return True

def setup_virtual_environment():
    """Create and activate virtual environment"""
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    if not run_command("python -m venv .venv", "Creating virtual environment"):
        return False
    
    # Instructions for activation (varies by OS)
    if os.name == 'nt':  # Windows
        activate_cmd = ".venv\\Scripts\\activate"
    else:  # macOS/Linux
        activate_cmd = "source .venv/bin/activate"
    
    print(f"📋 To activate virtual environment, run: {activate_cmd}")
    return True

def install_dependencies():
    """Install required dependencies"""
    pip_cmd = ".venv/bin/pip" if os.name != 'nt' else ".venv\\Scripts\\pip"
    
    commands = [
        (f"{pip_cmd} install --upgrade pip", "Upgrading pip"),
        (f"{pip_cmd} install -r requirements.txt", "Installing project dependencies")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def create_data_directories():
    """Create necessary directories for the project"""
    directories = ["models", "data", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    """Main setup function"""
    print("🏎️  F1 Race Position Predictor - Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup virtual environment
    if not setup_virtual_environment():
        print("❌ Failed to set up virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create directories
    create_data_directories()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate virtual environment:")
    if os.name == 'nt':
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print("2. Run the predictor:")
    print("   python improved_race_prediction_driver.py")
    
if __name__ == "__main__":
    main() 