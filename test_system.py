#!/usr/bin/env python3
"""
Test script to verify Clinical RAG system components
FREE version using local models only
"""
import sys
import os


def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")
    
    all_good = True
    
    # Test core packages
    try:
        import chromadb
        print("  ✓ chromadb")
    except ImportError:
        print("  ✗ chromadb - Run: pip install chromadb")
        all_good = False
    
    try:
        from dotenv import load_dotenv
        print("  ✓ python-dotenv")
    except ImportError:
        print("  ✗ python-dotenv - Run: pip install python-dotenv")
        all_good = False
    
    # Test FREE version packages
    try:
        from sentence_transformers import SentenceTransformer
        print("  ✓ sentence-transformers")
    except ImportError:
        print("  ✗ sentence-transformers - Run: pip install sentence-transformers")
        all_good = False
    
    try:
        import requests
        print("  ✓ requests")
    except ImportError:
        print("  ✗ requests - Run: pip install requests")
        all_good = False
    
    return all_good


def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    
    try:
        from config import config
        print("  ✓ config module loaded")
        
        # Check FREE version settings
        print(f"  ℹ Mode: FREE (local models)")
        print(f"    Ollama Model: {config.OLLAMA_MODEL}")
        print(f"    Ollama URL: {config.OLLAMA_BASE_URL}")
        print(f"    Embedding Model: {config.LOCAL_EMBEDDING_MODEL}")
        print(f"  ✓ Retrieval K: {config.RETRIEVAL_K}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error loading config: {e}")
        return False


def test_modules():
    """Test individual modules"""
    print("\nTesting modules...")
    
    try:
        from chunker import ClinicalNoteChunker
        print("  ✓ chunker module")
    except Exception as e:
        print(f"  ✗ chunker module: {e}")
        return False
    
    try:
        from retriever import ClinicalRAGRetriever
        print("  ✓ retriever module")
    except Exception as e:
        print(f"  ✗ retriever module: {e}")
        return False
    
    try:
        from generator import ClinicalGenerator
        print("  ✓ generator module")
    except Exception as e:
        print(f"  ✗ generator module: {e}")
        return False
    
    try:
        from pipeline import ClinicalRAGPipeline
        print("  ✓ pipeline module")
    except Exception as e:
        print(f"  ✗ pipeline module: {e}")
        return False
    
    return True


def test_chunker():
    """Test chunker functionality"""
    print("\nTesting chunker...")
    
    try:
        from chunker import ClinicalNoteChunker
        
        sample_note = """
Chief Complaint:
Fever and cough

History of Present Illness:
Patient presents with 3 days of fever and productive cough.

Physical Exam:
Lungs: crackles in right base
"""
        
        chunker = ClinicalNoteChunker()
        chunks = chunker.process_note(sample_note, patient_id="TEST")
        
        print(f"  ✓ Generated {len(chunks)} chunks")
        
        if len(chunks) > 0:
            print(f"  ✓ First chunk ID: {chunks[0]['chunk_id']}")
            print(f"  ✓ First section: {chunks[0]['section']}")
            return True
        else:
            print("  ✗ No chunks generated")
            return False
            
    except Exception as e:
        print(f"  ✗ Chunker error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 70)
    print("Clinical RAG System - Component Tests (FREE Version)")
    print("=" * 70)
    
    results = []
    
    # Test imports
    results.append(("Imports", test_imports()))
    
    # Test config
    results.append(("Configuration", test_config()))
    
    # Test modules
    results.append(("Modules", test_modules()))
    
    # Test chunker
    results.append(("Chunker", test_chunker()))
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print("✅ All tests passed! System is ready to use.")
        print("\nRun the demo:")
        print("  python main.py --demo")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        return 0
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Start Ollama: ollama serve")
        print("  3. Pull model: ollama pull llama3.2")
        return 1


if __name__ == "__main__":
    sys.exit(main())
