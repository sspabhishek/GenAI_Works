#!/usr/bin/env python3
"""
Configuration validation script
Run this to check if your setup is correct before running the app
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required = {
        'flask': 'Flask',
        'dotenv': 'python-dotenv',
        'requests': 'requests',
        'sentence_transformers': 'SentenceTransformer',
        'chromadb': 'ChromaDB',
        'numpy': 'NumPy'
    }

    print("\nChecking dependencies...")
    all_ok = True

    for module, name in required.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} NOT INSTALLED")
            all_ok = False

    if not all_ok:
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")

    return all_ok

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\nChecking .env file...")

    if not Path('.env').exists():
        print("  ❌ .env file not found")
        print("     Create it by copying .env.example:")
        print("     cp .env.example .env")
        return False

    print("  ✅ .env file exists")

    # Load env file
    from dotenv import load_dotenv
    load_dotenv()

    required_vars = [
        'ANTHROPIC_API_KEY',
        'LLM_ENDPOINT',
        'LLM_MODEL'
    ]

    all_ok = True
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == 'your_api_key_here':
            print(f"  ⚠️  {var} not configured or placeholder value")
            all_ok = False
        else:
            # Show masked value
            if var == 'ANTHROPIC_API_KEY':
                masked = value[:7] + '*' * 20 + value[-7:] if len(value) > 14 else '*' * 10
            else:
                masked = value
            print(f"  ✅ {var} = {masked}")

    return all_ok

def check_folders():
    """Check if necessary folders exist"""
    print("\nChecking folders...")

    folders = {
        'templates': 'templates/',
        'static': 'static/',
    }

    all_ok = True
    for name, path in folders.items():
        if Path(path).exists():
            print(f"  ✅ {path}")
        else:
            print(f"  ❌ {path} NOT FOUND")
            all_ok = False

    return all_ok

def check_files():
    """Check if all necessary files exist"""
    print("\nChecking files...")

    files = {
        'Flask app': 'app.py',
        'HTML template': 'templates/index.html',
        'CSS styling': 'static/style.css',
        'Requirements': 'requirements.txt',
    }

    all_ok = True
    for name, path in files.items():
        if Path(path).exists():
            print(f"  ✅ {name} ({path})")
        else:
            print(f"  ❌ {name} ({path}) NOT FOUND")
            all_ok = False

    return all_ok

def check_api_connection():
    """Test connection to Anthropic API"""
    print("\nChecking API connectivity...")

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('ANTHROPIC_API_KEY')
    endpoint = os.getenv('LLM_ENDPOINT')
    model = os.getenv('LLM_MODEL')

    if api_key == 'your_api_key_here' or not api_key:
        print("  ⚠️  API key not configured - skipping connectivity check")
        return False

    try:
        import requests

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01'
        }

        # Test with a simple request
        payload = {
            'model': model,
            'max_tokens': 100,
            'messages': [
                {'role': 'user', 'content': 'Say hello'}
            ]
        }

        response = requests.post(endpoint, headers=headers, json=payload, timeout=10)

        if response.status_code == 401:
            print("  ❌ API Authentication failed - check your API key")
            return False
        elif response.status_code == 404:
            print("  ❌ Endpoint or model not found - check LLM_ENDPOINT and LLM_MODEL")
            return False
        elif response.status_code == 200:
            print(f"  ✅ Connected to {model}")
            return True
        else:
            print(f"  ⚠️  Unexpected response: {response.status_code}")
            return False

    except requests.exceptions.Timeout:
        print("  ⚠️  Request timed out - API may be slow")
        return False
    except requests.exceptions.ConnectionError:
        print("  ⚠️  Connection error - check internet connection")
        return False
    except Exception as e:
        print(f"  ⚠️  Error: {str(e)}")
        return False

def main():
    """Run all checks"""
    print("=" * 50)
    print("GenAI Knowledge Assistant - Configuration Check")
    print("=" * 50)

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Folders", check_folders),
        ("Files", check_files),
        (".env File", check_env_file),
        ("API Connection", check_api_connection),
    ]

    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n❌ Error checking {name}: {str(e)}")
            results[name] = False

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)

    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")

    all_passed = all(results.values())

    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All checks passed! Ready to run:")
        print("\n   python app.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  • Install dependencies: pip install -r requirements.txt")
        print("  • Add API key to .env file")
        print("  • Check internet connection")
    print("=" * 50)

    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
