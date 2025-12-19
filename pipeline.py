"""
FREE End-to-end Clinical RAG Pipeline using local models
NO OpenAI API required - 100% FREE!
"""
import json
from typing import Dict, Optional
from chunker import ClinicalNoteChunker
from retriever import ClinicalRAGRetriever
from generator import ClinicalGenerator
from config import config


class ClinicalRAGPipeline:
    """Complete FREE pipeline for clinical note analysis"""
    
    def __init__(self):
        self.chunker = ClinicalNoteChunker()
        self.retriever = ClinicalRAGRetriever()
        self.generator = ClinicalGenerator()
        print("✓ Initialized FREE Clinical RAG Pipeline (no API costs!)")
    
    def index_note(self, note: str, patient_id: str = None):
        """
        Index a clinical note into the vector database
        
        Args:
            note: Clinical note text
            patient_id: Optional patient identifier
        """
        # Chunk the note
        chunks = self.chunker.process_note(note, patient_id=patient_id)
        
        # Add to vector database
        self.retriever.add_chunks(chunks)
        
        print(f"Indexed {len(chunks)} chunks for patient {patient_id or 'unknown'}")
        return chunks
    
    def analyze_note(
        self, 
        note: str = None, 
        patient_id: str = None,
        use_indexed: bool = False,
        retrieval_k: int = None
    ) -> Dict:
        """
        Analyze a clinical note and generate summary + differential diagnoses
        Uses FREE local models - no API costs!
        
        Args:
            note: Clinical note text (if not using indexed notes)
            patient_id: Optional patient identifier
            use_indexed: If True, retrieve from indexed notes; else index the provided note first
            retrieval_k: Number of chunks to retrieve
        
        Returns:
            Structured JSON output with summary and differential diagnoses
        """
        # Step 1: Index the note if needed
        if not use_indexed and note:
            self.index_note(note, patient_id)
        
        # Step 2: Retrieve relevant chunks
        query = config.RETRIEVAL_QUERY_TEMPLATE + \
                f" Patient ID: {patient_id or 'unknown'}"
        
        k = retrieval_k or config.RETRIEVAL_K
        chunks = self.retriever.retrieve(query, k=k)
        
        print(f"Retrieved {len(chunks)} chunks")
        
        # Step 3: Generate clinical output (FREE!)
        result = self.generator.generate_clinical_output(chunks, patient_id=patient_id)
        
        return result
    
    def clear_index(self):
        """Clear the vector database"""
        self.retriever.clear_collection()
    
    def initialize_collection(self):
        """Initialize a fresh collection"""
        self.retriever.create_collection()


def main():
    """Main demo function - FREE version!"""
    
    # Sample clinical note
    clinical_note = """
Chief Complaint:
Fever, cough, and shortness of breath

History of Present Illness:
Mr. Sharma, 65-year-old male, presents with fever (38.9°C), productive cough with yellow sputum, and shortness of breath for 3 days. Patient reports progressive worsening of dyspnea on exertion. Denies chest pain, but reports feeling weak and fatigued. No recent travel. Patient is a former smoker (20 pack-years, quit 5 years ago).

Past Medical History:
Type 2 Diabetes Mellitus (controlled on metformin)
Hypertension (controlled on lisinopril)
Hyperlipidemia

Medications:
Metformin 1000mg BID
Lisinopril 10mg daily
Atorvastatin 20mg daily

Allergies:
Penicillin (rash)

Vital Signs:
Temperature: 38.9°C (102°F)
Blood Pressure: 135/85 mmHg
Heart Rate: 98 bpm
Respiratory Rate: 24/min
SpO2: 91% on room air

Physical Exam:
General: Alert, oriented, appears ill and in mild respiratory distress
HEENT: Normal
Neck: No lymphadenopathy
Lungs: Decreased breath sounds in right lower lobe, crackles present on auscultation
Heart: Regular rate and rhythm, no murmurs
Abdomen: Soft, non-tender
Extremities: No edema

Laboratory:
WBC: 16.5 x10^9/L (elevated, reference 4-11)
Neutrophils: 82% (elevated)
CRP: 120 mg/L (elevated, reference <10)
Procalcitonin: 2.5 ng/mL (elevated, reference <0.5)
Blood glucose: 145 mg/dL
Creatinine: 1.0 mg/dL (normal)

Imaging:
Chest X-ray (PA and Lateral):
- Right lower lobe consolidation consistent with lobar pneumonia
- No pleural effusion
- No pneumothorax
- Cardiac silhouette normal

Assessment and Plan:
65-year-old male with clinical and radiographic findings consistent with community-acquired pneumonia (CAP). Given penicillin allergy, will initiate treatment with respiratory fluoroquinolone. Close monitoring required given age and comorbidities.
"""
    
    print("=" * 70)
    print("🆓 FREE Clinical RAG Pipeline - Demo (No API Costs!)")
    print("=" * 70)
    print("\n💰 Cost: $0.00 - Using 100% FREE local models!")
    print("🔒 Privacy: 100% local - your data never leaves this computer\n")
    
    # Initialize pipeline
    pipeline = ClinicalRAGPipeline()
    pipeline.initialize_collection()
    
    # Analyze the note
    print("\nAnalyzing clinical note with FREE local models...")
    result = pipeline.analyze_note(
        note=clinical_note,
        patient_id="PT001",
        use_indexed=False
    )
    
    # Display results
    print("\n" + "=" * 70)
    print("RESULTS (Generated by FREE Local Models)")
    print("=" * 70)
    
    print(f"\n📋 Patient ID: {result.get('patient_id', 'Unknown')}")
    
    print("\n--- SUMMARY ---")
    if 'summary' in result and 'text' in result['summary']:
        for i, bullet in enumerate(result['summary']['text'], 1):
            print(f"{i}. {bullet}")
    
    print("\n--- DIFFERENTIAL DIAGNOSES ---")
    if 'differential' in result:
        for dx in result['differential']:
            print(f"\n{dx.get('rank', '?')}. {dx.get('diagnosis', 'Unknown')}")
            print(f"   Confidence: {dx.get('confidence', 0.0):.2f}")
            print(f"   Rationale: {dx.get('rationale', 'N/A')}")
            if 'supporting_evidence' in dx and dx['supporting_evidence']:
                print(f"   Evidence: {len(dx['supporting_evidence'])} citation(s)")
    
    if 'warnings' in result and result['warnings']:
        print("\n--- WARNINGS ---")
        for warning in result['warnings']:
            print(f"  ⚠ {warning}")
    
    print("\n--- METADATA ---")
    if 'model_metadata' in result:
        for key, value in result['model_metadata'].items():
            print(f"  {key}: {value}")
    
    # Save to file
    output_file = "output_free_pneumonia_case.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\n✅ Full output saved to: {output_file}")
    print("\n💰 Total cost: $0.00 (FREE!)")
    print("🔒 All processing done locally - maximum privacy!")


if __name__ == "__main__":
    main()
