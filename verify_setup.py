"""
Configuration Verification Script
For checking if environment configuration is correct
"""

import os
import sys


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   ✗ Python version too low, requires Python 3.8 or higher")
        return False
    else:
        print("   ✓ Python version meets requirements")
        return True


def check_dependencies():
    """Check if dependency packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = {
        'praw': 'praw',
        'dotenv': 'python-dotenv',
        'pandas': 'pandas',
        'tqdm': 'tqdm',
        'dateutil': 'python-dateutil'
    }
    
    all_installed = True
    
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ✗ {package} not installed")
            all_installed = False
    
    if not all_installed:
        print("\n   Tip: Run the following command to install dependencies:")
        print("   pip install -r requirements.txt")
    
    return all_installed


def check_env_file():
    """Check if .env file exists and contains necessary configuration"""
    print("\n🔧 Checking environment configuration...")
    
    if not os.path.exists('.env'):
        print("   ✗ .env file does not exist")
        print("   Tip: Copy .env.example to .env and fill in your Reddit API credentials")
        print("   Windows: copy .env.example .env")
        print("   Linux/Mac: cp .env.example .env")
        return False
    
    print("   ✓ .env file exists")
    
    # Try to load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = [
            'REDDIT_CLIENT_ID',
            'REDDIT_CLIENT_SECRET',
            'REDDIT_USER_AGENT'
        ]
        
        missing_vars = []
        placeholder_vars = []
        
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                missing_vars.append(var)
                print(f"   ✗ {var} not set")
            elif 'your_' in value.lower() or 'here' in value.lower():
                placeholder_vars.append(var)
                print(f"   ⚠ {var} is using placeholder value, please fill in real credentials")
            else:
                print(f"   ✓ {var} is set")
        
        if missing_vars or placeholder_vars:
            print("\n   Tip: Set these variables in the .env file")
            print("   Create a Reddit app at https://www.reddit.com/prefs/apps")
            return False
        
        return True
        
    except ImportError:
        print("   ⚠ Cannot check environment variables (python-dotenv not installed)")
        return False


def check_output_dir():
    """Check output directory"""
    print("\n📁 Checking output directory...")
    
    if os.path.exists('output'):
        print("   ✓ output directory exists")
    else:
        print("   ℹ output directory does not exist (will be created automatically on first run)")
    
    return True


def main():
    """Main function"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║      Reddit Topic Tracker - Configuration Verification      ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_env_file(),
        check_output_dir()
    ]
    
    print("\n" + "="*60)
    if all(checks[:3]):  # First three checks must pass
        print("✅ All checks passed! You can start using the tracker.")
        print("\nUsage example:")
        print('python tracker.py --keyword "artificial intelligence" --subreddit "MachineLearning" --limit 50')
    else:
        print("❌ Configuration check failed, please follow the tips above to fix issues.")
        print("\nConfiguration steps:")
        print("1. Ensure Python 3.8 or higher is installed")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Create .env file and fill in Reddit API credentials")
        print("4. Register an app at https://www.reddit.com/prefs/apps to get credentials")
    print("="*60)


if __name__ == '__main__':
    main()
