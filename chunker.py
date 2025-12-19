"""
Document chunking and preprocessing module for clinical notes
"""
import re
from typing import List, Dict, Tuple
from config import config


class ClinicalNoteChunker:
    """Chunks clinical notes into sections with metadata"""
    
    # Common clinical note sections
    SECTION_PATTERNS = [
        r"(?i)^(Chief Complaint|CC):",
        r"(?i)^(History of Present Illness|HPI):",
        r"(?i)^(Past Medical History|PMH):",
        r"(?i)^(Medications|MEDS):",
        r"(?i)^(Allergies):",
        r"(?i)^(Physical Exam|PE):",
        r"(?i)^(Vital Signs|VS):",
        r"(?i)^(Laboratory|Labs|Lab Results):",
        r"(?i)^(Imaging|Radiology):",
        r"(?i)^(Assessment|A&P|Assessment and Plan):",
        r"(?i)^(Plan):",
        r"(?i)^(Differential Diagnosis|DDx):",
    ]
    
    def __init__(self, chunk_size: int = None, overlap: int = None):
        self.chunk_size = chunk_size or config.CHUNK_SIZE
        self.overlap = overlap or config.CHUNK_OVERLAP
    
    def extract_sections(self, note: str) -> List[Dict[str, str]]:
        """Extract sections from clinical note"""
        sections = []
        lines = note.split('\n')
        current_section = "UNKNOWN"
        current_text = []
        
        for line in lines:
            # Check if line starts a new section
            is_section_header = False
            for pattern in self.SECTION_PATTERNS:
                if re.match(pattern, line.strip()):
                    # Save previous section
                    if current_text:
                        sections.append({
                            "section": current_section,
                            "text": '\n'.join(current_text).strip()
                        })
                    
                    # Start new section
                    current_section = line.strip().rstrip(':')
                    current_text = []
                    is_section_header = True
                    break
            
            if not is_section_header and line.strip():
                current_text.append(line)
        
        # Add last section
        if current_text:
            sections.append({
                "section": current_section,
                "text": '\n'.join(current_text).strip()
            })
        
        return sections
    
    def chunk_text(self, text: str, max_size: int) -> List[str]:
        """Split text into chunks of max_size with overlap"""
        words = text.split()
        chunks = []
        
        if len(words) <= max_size:
            return [text]
        
        start = 0
        while start < len(words):
            end = min(start + max_size, len(words))
            chunk = ' '.join(words[start:end])
            chunks.append(chunk)
            
            if end >= len(words):
                break
            
            start = end - self.overlap
        
        return chunks
    
    def process_note(self, note: str, patient_id: str = None) -> List[Dict[str, str]]:
        """
        Process clinical note into chunks with metadata
        
        Returns:
            List of dicts with: chunk_id, section, text, patient_id
        """
        sections = self.extract_sections(note)
        chunks = []
        chunk_counter = 0
        
        for section_data in sections:
            section_name = section_data["section"]
            section_text = section_data["text"]
            
            # Chunk the section text if it's too long
            text_chunks = self.chunk_text(section_text, self.chunk_size)
            
            for chunk_text in text_chunks:
                chunk_counter += 1
                chunks.append({
                    "chunk_id": f"chunk_{chunk_counter}",
                    "section": section_name,
                    "text": chunk_text,
                    "patient_id": patient_id or "unknown"
                })
        
        return chunks
    
    def format_chunks_for_prompt(self, chunks: List[Dict[str, str]]) -> str:
        """Format chunks for LLM prompt"""
        formatted = []
        for chunk in chunks:
            formatted.append(
                f"CHUNK_ID: {chunk['chunk_id']}\n"
                f"SECTION: {chunk['section']}\n"
                f"TEXT: {chunk['text']}\n"
            )
        return '\n'.join(formatted)


if __name__ == "__main__":
    # Test the chunker
    sample_note = """
Chief Complaint:
Fever, cough, and shortness of breath

History of Present Illness:
Mr. Sharma, 65-year-old male, presents with fever (38.9°C), productive cough, and shortness of breath for 3 days. Patient reports worsening dyspnea on exertion.

Physical Exam:
Lungs: Decreased breath sounds in right lower lobe, crackles present.

Laboratory:
WBC 16.5 x10^9/L (elevated), CRP 120 mg/L (elevated).

Imaging:
Chest X-ray shows right lower lobe consolidation consistent with lobar pneumonia.
"""
    
    chunker = ClinicalNoteChunker()
    chunks = chunker.process_note(sample_note, patient_id="PT001")
    
    print(f"Generated {len(chunks)} chunks:")
    for chunk in chunks:
        print(f"\n{chunk['chunk_id']} ({chunk['section']}):")
        print(f"  {chunk['text'][:100]}...")
