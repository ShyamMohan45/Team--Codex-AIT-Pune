#!/usr/bin/env python3
"""
Pre-flight check script for Clinical RAG System
Run this before your first use to verify setup
"""
import sys
import os
from pathlib import Path


def check_python_version():
    """Check Python version is 3.8+"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor} (Need 3.8+)")
        return False


def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...")
    required = [
        'chromadb',
        'sentence_transformers',
        'dotenv',
        'requests',
        'numpy'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (MISSING)")
            missing.append(package)
    
    if missing:
        print(f"\n  ⚠ Missing packages: {', '.join(missing)}")
        print("  Run: pip install -r requirements.txt")
        return False
    return True


def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\n🔍 Checking .env configuration...")
    
    if not Path('.env').exists():
        print("  ✗ .env file not found")
        if Path('.env.example').exists():
            print("  💡 Tip: Copy .env.example to .env")
            print("     cp .env.example .env")
        return False
    
    print("  ✓ .env file exists")
    
    # Check for API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OLLAMA_API_KEY')
    base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    
    if 'ollama.com' in base_url:
        if api_key and api_key != 'your_api_key_here':
            print("  ✓ OLLAMA_API_KEY is set")
            return True
        else:
            print("  ⚠ OLLAMA_API_KEY not configured")
            print("  💡 Get your free key at: https://ollama.com/settings/keys")
            print("     Then edit .env and set: OLLAMA_API_KEY=your_key")
            return False
    else:
        print("  ℹ Using local Ollama (no API key needed)")
        return True


def check_ollama():
    """Check if Ollama is accessible"""
    print("\n🔍 Checking Ollama connection...")
    
    try:
        import requests
        from dotenv import load_dotenv
        load_dotenv()
        
        base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        api_key = os.getenv('OLLAMA_API_KEY')
        
        headers = {'Content-Type': 'application/json'}
        if api_key and 'ollama.com' in base_url:
            headers['Authorization'] = f'Bearer {api_key}'
        
        response = requests.get(f"{base_url}/api/tags", headers=headers, timeout=5)
        
        if response.status_code == 200:
            print(f"  ✓ Connected to Ollama at {base_url}")
            models = response.json().get('models', [])
            if models:
                model_names = [m['name'] for m in models]
                print(f"  ✓ Available models: {', '.join(model_names[:3])}...")
            return True
        else:
            print(f"  ✗ Ollama returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"  ✗ Cannot connect to Ollama")
        if 'ollama.com' in os.getenv('OLLAMA_BASE_URL', ''):
            print("  💡 Check your internet connection and API key")
        else:
            print("  💡 Start Ollama: ollama serve")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def check_project_structure():
    """Check if all required files exist"""
    print("\n🔍 Checking project structure...")
    
    required_files = [
        'main.py',
        'pipeline.py',
        'chunker.py',
        'retriever.py',
        'generator.py',
        'config.py',
        'sample_notes.py',
        'requirements.txt',
        'README.md'
    ]
    
    missing = []
    for file in required_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (MISSING)")
            missing.append(file)
    
    if missing:
        print(f"\n  ⚠ Missing files: {', '.join(missing)}")
        return False
    return True


def main():
    """Run all checks"""
    print("=" * 70)
    print("Clinical RAG System - Pre-flight Check")
    print("=" * 70)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Environment Config", check_env_file),
        ("Ollama Connection", check_ollama),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n  ✗ Error during {name} check: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    
    passed = sum(results.values())
    total = len(results)
    
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {name}")
    
    print("\n" + "=" * 70)
    
    if passed == total:
        print("✅ All checks passed! You're ready to go!")
        print("\nNext steps:")
        print("  1. Activate virtual environment: source venv/bin/activate")
        print("  2. Run demo: python3 main.py --demo")
        return 0
    else:
        print(f"⚠ {total - passed} check(s) failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Missing dependencies: pip install -r requirements.txt")
        print("  - Missing .env: cp .env.example .env")
        print("  - Ollama not running: ollama serve (for local)")
        print("  - Missing API key: Edit .env and add your Ollama Cloud key")
        return 1


if __name__ == "__main__":
    sys.exit(main())
