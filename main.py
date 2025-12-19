#!/usr/bin/env python3
"""
Clinical RAG System - Main CLI Interface
Works with both FREE (local) and PAID (OpenAI) versions
"""
import argparse
import json
import sys
from pathlib import Path
from pipeline import ClinicalRAGPipeline
from sample_notes import get_sample_note, list_cases
from config import config


def run_demo(case_name: str = "pneumonia_case", output_file: str = None):
    """Run the demo with a sample case"""
    print("=" * 70)
    print("Clinical RAG System - Demo Mode")
    print("🆓 Mode: FREE (Local Models)")
    print("💰 Cost: $0.00")
    print("=" * 70)
    
    # Get sample note
    print(f"\nLoading sample case: {case_name}")
    note = get_sample_note(case_name)
    
    if not note:
        print(f"Error: Case '{case_name}' not found.")
        print(f"Available cases: {', '.join(list_cases())}")
        return
    
    print(f"Note length: {len(note)} characters")
    
    # Initialize pipeline
    print("\nInitializing Clinical RAG pipeline...")
    pipeline = ClinicalRAGPipeline()
    pipeline.initialize_collection()
    
    # Analyze
    print("\nAnalyzing clinical note...")
    patient_id = case_name.upper().replace("_", "-")
    result = pipeline.analyze_note(
        note=note,
        patient_id=patient_id,
        use_indexed=False
    )
    
    # Display results
    display_results(result)
    
    # Save output
    if output_file:
        save_output(result, output_file)
    else:
        save_output(result, f"output_{case_name}.json")


def run_custom(note_file: str, patient_id: str = None, output_file: str = None):
    """Run with a custom clinical note file"""
    print("=" * 70)
    print("Clinical RAG System - Custom Note Analysis")
    print("=" * 70)
    
    # Read note
    note_path = Path(note_file)
    if not note_path.exists():
        print(f"Error: File '{note_file}' not found.")
        return
    
    print(f"\nReading note from: {note_file}")
    with open(note_path, 'r') as f:
        note = f.read()
    
    print(f"Note length: {len(note)} characters")
    
    # Initialize pipeline
    print("\nInitializing Clinical RAG pipeline...")
    pipeline = ClinicalRAGPipeline()
    pipeline.initialize_collection()
    
    # Analyze
    print("\nAnalyzing clinical note...")
    result = pipeline.analyze_note(
        note=note,
        patient_id=patient_id or "CUSTOM",
        use_indexed=False
    )
    
    # Display results
    display_results(result)
    
    # Save output
    if output_file:
        save_output(result, output_file)
    else:
        save_output(result, "output_custom.json")


def display_results(result: dict):
    """Display results in a formatted way"""
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    # Patient ID
    print(f"\n📋 Patient ID: {result.get('patient_id', 'Unknown')}")
    
    # Summary
    print("\n" + "─" * 70)
    print("📝 CLINICAL SUMMARY")
    print("─" * 70)
    if 'summary' in result and 'text' in result['summary']:
        for i, bullet in enumerate(result['summary']['text'], 1):
            print(f"  {i}. {bullet}")
        
        if 'supporting_evidence' in result['summary']:
            evidence_count = len(result['summary']['supporting_evidence'])
            print(f"\n  Evidence citations: {evidence_count}")
    else:
        print("  No summary generated.")
    
    # Differential Diagnoses
    print("\n" + "─" * 70)
    print("🔍 DIFFERENTIAL DIAGNOSES")
    print("─" * 70)
    if 'differential' in result and result['differential']:
        for dx in result['differential']:
            rank = dx.get('rank', '?')
            diagnosis = dx.get('diagnosis', 'Unknown')
            confidence = dx.get('confidence', 0.0)
            
            # Create confidence bar
            bar_length = 20
            filled = int(confidence * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            print(f"\n  {rank}. {diagnosis}")
            print(f"     Confidence: [{bar}] {confidence:.2%}")
            print(f"     Rationale: {dx.get('rationale', 'N/A')}")
            
            if 'supporting_evidence' in dx:
                print(f"     Citations: {len(dx['supporting_evidence'])} chunk(s)")
                for i, ev in enumerate(dx['supporting_evidence'][:2], 1):  # Show first 2
                    quote = ev.get('quote', '')[:60]
                    print(f"       └─ {ev.get('chunk_id', '?')}: \"{quote}...\"")
    else:
        print("  No differential diagnoses generated.")
    
    # Warnings
    if 'warnings' in result and result['warnings']:
        print("\n" + "─" * 70)
        print("⚠️  WARNINGS")
        print("─" * 70)
        for warning in result['warnings']:
            print(f"  • {warning}")
    
    # Metadata
    print("\n" + "─" * 70)
    print("ℹ️  METADATA")
    print("─" * 70)
    if 'model_metadata' in result:
        for key, value in result['model_metadata'].items():
            print(f"  {key}: {value}")


def save_output(result: dict, filename: str):
    """Save results to JSON file"""
    output_path = Path(filename)
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\n✅ Full output saved to: {output_path.absolute()}")


def main():
    parser = argparse.ArgumentParser(
        description="Clinical RAG System - AI-powered clinical note analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run demo with default case (pneumonia)
  python main.py --demo
  
  # Run demo with specific case
  python main.py --demo --case mi_case
  
  # Analyze custom note file
  python main.py --file my_note.txt --patient-id PT123
  
  # List available demo cases
  python main.py --list-cases
        """
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run demo mode with sample cases'
    )
    
    parser.add_argument(
        '--case',
        type=str,
        default='pneumonia_case',
        help='Sample case to use in demo mode (default: pneumonia_case)'
    )
    
    parser.add_argument(
        '--file',
        type=str,
        help='Path to custom clinical note file'
    )
    
    parser.add_argument(
        '--patient-id',
        type=str,
        help='Patient ID for custom note'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Output JSON file path'
    )
    
    parser.add_argument(
        '--list-cases',
        action='store_true',
        help='List available sample cases'
    )
    
    args = parser.parse_args()
    
    # List cases
    if args.list_cases:
        print("\nAvailable sample cases:")
        for i, case in enumerate(list_cases(), 1):
            print(f"  {i}. {case}")
        return
    
    # Run demo
    if args.demo:
        run_demo(args.case, args.output)
        return
    
    # Run custom
    if args.file:
        run_custom(args.file, args.patient_id, args.output)
        return
    
    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
