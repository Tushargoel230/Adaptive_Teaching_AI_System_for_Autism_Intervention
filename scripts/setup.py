#!/usr/bin/env python3
"""
Setup script for Adaptive Teaching AI System.
Helps configure environment and download necessary data.
"""

import os
import sys
import shutil
from pathlib import Path
import subprocess

def create_directories():
    """Create necessary project directories"""
    print("Creating project directories...")
    directories = [
        './data',
        './data/annotations',
        './data/MMASD',
        './logs',
        './logs/sessions',
        './models',
        './models/checkpoints',
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}")
    print("Directories created.\n")

def create_env_file():
    """Create .env file from template"""
    print("Setting up environment configuration...")
    
    if Path('.env').exists():
        print("  .env file already exists, skipping...")
        return
    
    if not Path('.env.example').exists():
        print("  ERROR: .env.example not found!")
        return
    
    # Copy template
    shutil.copy('.env.example', '.env')
    print("  ✓ Created .env file from template")
    
    # Prompt for API key
    print("\n  Configure your environment variables:")
    print("  1. Edit .env file")
    print("  2. Add your OpenAI API key: OPENAI_API_KEY=sk-...")
    print("  3. Save the file\n")

def check_dependencies():
    """Check if required packages are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        'numpy',
        'opencv-cv2',
        'torch',
        'mediapipe',
        'transformers',
        'openai',
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n  Missing packages: {', '.join(missing)}")
        print("  Install with: pip install -r requirements.txt\n")
    else:
        print("  All dependencies installed.\n")

def download_mmasd_info():
    """Provide info on downloading MMASD dataset"""
    print("MMASD Dataset Information:")
    print("  The MMASD (Multimodal Autism Behavior Analysis) dataset contains:")
    print("  - 6+ hours of therapy sessions with children with autism")
    print("  - Video recordings with behavioral annotations")
    print("  - Available at: [provide actual link if public]")
    print("\n  To download:")
    print("  1. Visit the dataset repository")
    print("  2. Download and extract to ./data/MMASD/")
    print("  3. Run: python scripts/prepare_dataset.py\n")

def setup_logging():
    """Create logging directory structure"""
    print("Setting up logging...")
    
    log_dir = Path('./logs')
    log_dir.mkdir(exist_ok=True)
    
    # Create empty log files
    (log_dir / 'teaching_ai.log').touch(exist_ok=True)
    (log_dir / 'sessions').mkdir(exist_ok=True)
    
    print("  ✓ Logging directories ready\n")

def test_installation():
    """Test if the system can be imported"""
    print("Testing installation...")
    
    try:
        from autism_teaching_ai import AdaptiveTeachingAI
        print("  ✓ Successfully imported AdaptiveTeachingAI")
        print("  ✓ Installation complete!\n")
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        print("  Install dependencies with: pip install -r requirements.txt\n")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("=" * 60)
    print("Setup Complete! Next steps:")
    print("=" * 60)
    print("\n1. Configure Environment:")
    print("   - Edit .env file with your OpenAI API key")
    print("   - See .env.example for all available options\n")
    
    print("2. Test Installation:")
    print("   python scripts/test_system.py\n")
    
    print("3. Run Demo:")
    print("   python demo.py\n")
    
    print("4. (Optional) Download MMASD Dataset:")
    print("   - Download from dataset repository")
    print("   - Extract to ./data/MMASD/\n")
    
    print("5. Read Documentation:")
    print("   - autism_teaching_ai/README.md (component docs)")
    print("   - README.md (project overview)\n")
    
    print("=" * 60)

def main():
    """Run setup"""
    print("=" * 60)
    print("Adaptive Teaching AI System - Setup")
    print("=" * 60)
    print()
    
    try:
        create_directories()
        create_env_file()
        setup_logging()
        check_dependencies()
        download_mmasd_info()
        
        if test_installation():
            print_next_steps()
            return 0
        else:
            return 1
            
    except Exception as e:
        print(f"Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
