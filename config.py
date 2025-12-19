"""
Configuration module for Clinical RAG System
100% FREE - Uses local models only (Ollama + sentence-transformers)
"""
import os
from dotenv import load_dotenv

load_dotenv()


class LocalConfig:
    """Configuration for Clinical RAG System (Ollama Cloud or Local)"""
    
    # Ollama Configuration (Cloud or Local)
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
    OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", None)  # For Ollama Cloud
    
    # Local Embedding Configuration (FREE)
    LOCAL_EMBEDDING_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # Model Configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1200"))
    
    # Retrieval Configuration
    RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "10"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
    
    # Vector DB Configuration
    VECTOR_DB_PATH = "./chroma_db"
    COLLECTION_NAME = "clinical_notes"
    
    # Prompts
    SYSTEM_PROMPT = """You are a clinical assistant. Output ONLY valid JSON. No explanations, no thinking, just JSON."""

    RETRIEVAL_QUERY_TEMPLATE = """From the note(s), find chunks that best support:
1) a concise factual summary of the patient's current condition, and
2) the top differential diagnoses.

Query to embed/search: "Summarize the patient and list prioritized differential diagnoses with supporting evidence."
"""

    GENERATION_PROMPT_TEMPLATE = """Given these clinical note excerpts, produce a JSON object with a summary and differential diagnoses.

CHUNKS:
{chunks}

Output ONLY this JSON structure (no other text):
{{
  "patient_id": null,
  "summary": {{
    "text": ["bullet point 1", "bullet point 2", "bullet point 3"],
    "supporting_evidence": [{{"chunk_id":"chunk_1","offset":[0,50],"quote":"relevant text"}}]
  }},
  "differential": [
    {{
      "rank": 1,
      "diagnosis": "Diagnosis Name",
      "confidence": 0.95,
      "rationale": "brief explanation",
      "supporting_evidence": [{{"chunk_id":"chunk_2","offset":[0,30],"quote":"supporting text"}}],
      "evidence_score": 0.9
    }}
  ],
  "warnings": []
}}

Output JSON only:"""

    VERIFICATION_PROMPT_TEMPLATE = """VERIFIER:
Given one candidate rationale sentence and the full text of one cited chunk, return a numeric support score between 0.0 and 1.0 indicating how strongly the chunk entails/supports the sentence. Output only the number.

Input format:
RATIONALE: "{rationale}"
CHUNK_TEXT: "{chunk_text}"

Return: a single float (e.g., 0.87)"""


config = LocalConfig()
