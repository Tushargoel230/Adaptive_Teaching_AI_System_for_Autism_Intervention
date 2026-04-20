#!/usr/bin/env python3
"""
FASTEST SETUP - Get demo running in 90 seconds!

This script will:
1. Check if dependencies are installed
2. Set up .env file if needed
3. Launch live demo with your camera

Run: python quick_setup.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(text)
    print("="*60)

def check_command(cmd):
    """Check if command exists"""
    return subprocess.run(['which', cmd], capture_output=True).returncode == 0

def install_requirements():
    """Install pip requirements"""
    print("\n📦 Installing dependencies...")
    print("   This may take 2-3 minutes on first run...\n")
    result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print("⚠️  Some packages may have failed. Continuing anyway...")
    else:
        print("✓ Dependencies installed!")

def check_dependencies():
    """Check if key packages are installed"""
    packages = ['numpy', 'cv2', 'mediapipe']
    missing = []
    
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"  ✓ {pkg}")
        except ImportError:
            print(f"  ✗ {pkg} (will install)")
            missing.append(pkg)
    
    return missing

def setup_env_file():
    """Create .env file if it doesn't exist"""
    if Path('.env').exists():
        print("✓ .env file exists, skipping...")
        return
    
    if Path('.env.example').exists():
        import shutil
        shutil.copy('.env.example', '.env')
        print("✓ Created .env from template")
        
        # Optionally ask for API key
        print("\n🔑 OpenAI API Key Setup:")
        print("   Get free API key from: https://platform.openai.com/account/billing/overview")
        api_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
        
        if api_key:
            with open('.env', 'r') as f:
                content = f.read()
            content = content.replace('OPENAI_API_KEY=sk-your-api-key-here', f'OPENAI_API_KEY={api_key}')
            with open('.env', 'w') as f:
                f.write(content)
            print("   ✓ API key saved to .env")
        else:
            print("   ℹ️  Using mock LLM mode (no API key needed)")
            with open('.env', 'r') as f:
                content = f.read()
            content = content.replace('USE_MOCK_LLM=False', 'USE_MOCK_LLM=True')
            with open('.env', 'w') as f:
                f.write(content)

def check_camera():
    """Check if camera is available"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            cap.release()
            print("✓ Webcam detected!")
            return True
    except:
        pass
    
    print("⚠️  No webcam detected (will use mock data)")
    return False

def test_imports():
    """Test if system can be imported"""
    try:
        from autism_teaching_ai import AdaptiveTeachingAI
        print("✓ System imports successful!")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def launch_demo(use_camera=True):
    """Launch live demo"""
    cmd = [sys.executable, 'live_demo.py', '--duration', '30']
    
    if not use_camera:
        cmd.append('--mock')
    
    print("\n" + "="*60)
    print("🚀 LAUNCHING LIVE DEMO")
    print("="*60)
    print("\n📝 Instructions:")
    print("  • Your webcam will open")
    print("  • Real-time analysis shows in top-left corner")
    print("  • Press 'q' to quit")
    print("  • Press 'p' to pause/resume")
    print("\n▶️  Starting in 3 seconds...\n")
    
    time.sleep(3)
    
    subprocess.run(cmd)
    
    print("\n✓ Demo complete!")
    return True

def main():
    print_header("⚡ ADAPTIVE TEACHING AI - QUICK SETUP")
    
    # Step 1: Check if running in correct directory
    if not Path('autism_teaching_ai').exists():
        print("❌ Error: Run this from project root directory!")
        print("   cd /path/to/final_project")
        return 1
    
    # Step 2: Check Python version
    print(f"\n🐍 Python: {sys.version.split()[0]}")
    if sys.version_info < (3, 10):
        print("⚠️  Warning: Python 3.10+ recommended")
    else:
        print("✓ Python 3.10+ detected")
    
    # Step 3: Check dependencies
    print("\n📚 Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n❌ Missing: {', '.join(missing)}")
        print("\n📥 Installing requirements...")
        install_requirements()
    
    # Step 4: Setup environment
    print("\n⚙️  Setting up environment...")
    setup_env_file()
    
    # Step 5: Check camera
    print("\n📷 Checking camera...")
    has_camera = check_camera()
    
    # Step 6: Test imports
    print("\n🔗 Testing imports...")
    if not test_imports():
        print("\n⚠️  Import test failed. Installing requirements...")
        install_requirements()
        if not test_imports():
            print("❌ Still failing. Check installation.")
            return 1
    
    # All checks passed!
    print_header("✅ ALL CHECKS PASSED - READY TO DEMO!")
    
    print("\n📊 System Status:")
    print(f"  • Python: ✓")
    print(f"  • Dependencies: ✓")
    print(f"  • Webcam: {'✓' if has_camera else '✗ (will use mock)'}")
    print(f"  • Imports: ✓")
    
    # Launch demo
    print("\n🎬 Ready to launch live demo!")
    response = input("\nLaunch demo now? (y/n): ").strip().lower()
    
    if response == 'y':
        launch_demo(use_camera=has_camera)
    else:
        print("\n▶️  To run demo later:")
        if has_camera:
            print("   python live_demo.py --duration 30")
        else:
            print("   python live_demo.py --duration 30 --mock")
        print("\n💡 Or run static demo:")
        print("   python demo.py")
    
    print_header("✓ Setup Complete!")
    print("\n📝 Next steps:")
    print("  1. Run: python quick_setup.py (again)")
    print("  2. Or: python live_demo.py --duration 30")
    print("  3. Or: python demo.py")
    print("\n📄 For more info: see QUICK_DEMO_GUIDE.md")
    
    return 0

if __name__ == "__main__":
    exit(main())
