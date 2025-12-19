"""
LLM generation using Ollama (Cloud or Local)
Supports both Ollama Cloud (no GPU needed) and local Ollama
"""
import json
import requests
import os
from typing import List, Dict, Optional
from config import config
from chunker import ClinicalNoteChunker


class ClinicalGenerator:
    """Generate clinical summaries using Ollama (Cloud or Local)"""
    
    def __init__(self):
        self.base_url = config.OLLAMA_BASE_URL
        self.model = config.OLLAMA_MODEL
        self.api_key = getattr(config, 'OLLAMA_API_KEY', None)
        self.chunker = ClinicalNoteChunker()
        
        # Determine if using cloud or local
        self.is_cloud = 'ollama.com' in self.base_url
        
        # Check if Ollama is accessible
        self._check_ollama()
    
    def _get_headers(self):
        """Get headers for API requests"""
        headers = {'Content-Type': 'application/json'}
        if self.is_cloud and self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers
    
    def _check_ollama(self):
        """Check if Ollama is accessible"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                headers=self._get_headers()
            )
            if response.status_code == 200:
                mode = "Ollama Cloud" if self.is_cloud else "Local Ollama"
                print(f"✓ Connected to {mode} at {self.base_url}")
                models = response.json().get('models', [])
                if models:
                    print(f"✓ Available models: {[m['name'] for m in models]}")
            else:
                print(f"⚠ Ollama returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            if self.is_cloud:
                print(f"⚠ WARNING: Cannot connect to Ollama Cloud")
                print(f"  Check your API key and internet connection")
            else:
                print(f"⚠ WARNING: Cannot connect to Ollama at {self.base_url}")
                print("  Please start Ollama: ollama serve")
    
    def format_chunks_for_prompt(self, chunks: List[Dict[str, str]]) -> str:
        """Format chunks for the generation prompt"""
        formatted = []
        for chunk in chunks:
            formatted.append(
                f"CHUNK_ID: {chunk['chunk_id']}\n"
                f"SECTION: {chunk['section']}\n"
                f"TEXT: {chunk['text']}\n"
            )
        return '\n'.join(formatted)
    
    def generate_clinical_output(
        self, 
        chunks: List[Dict[str, str]], 
        patient_id: str = None
    ) -> Dict:
        """
        Generate clinical summary and differential diagnoses from chunks
        Using FREE local LLM via Ollama
        
        Args:
            chunks: List of retrieved chunks
            patient_id: Optional patient identifier
        
        Returns:
            Structured JSON output with summary and differential diagnoses
        """
        # Format chunks for prompt
        chunks_text = self.format_chunks_for_prompt(chunks)
        
        # Build the generation prompt
        user_prompt = config.GENERATION_PROMPT_TEMPLATE.format(chunks=chunks_text)
        full_prompt = f"{config.SYSTEM_PROMPT}\n\n{user_prompt}"
        
        # Call Ollama API
        try:
            mode_desc = "Ollama Cloud" if self.is_cloud else "local"
            print(f"Generating with {self.model} ({mode_desc} model)...")
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                headers=self._get_headers(),
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": config.TEMPERATURE,
                        "num_predict": config.MAX_TOKENS
                    }
                },
                timeout=180  # Longer timeout for cloud/large models
            )
            
            if response.status_code != 200:
                print(f"ERROR: Ollama API returned status {response.status_code}")
                print(f"Response: {response.text[:500]}")
                raise Exception(f"Ollama API returned status {response.status_code}: {response.text}")
            
            response_data = response.json()
            
            # Get the generated text - try multiple fields
            generated_text = ''
            thinking_text = ''
            
            if response_data.get('response'):
                generated_text = response_data['response']
                print(f"DEBUG: Got response field ({len(generated_text)} chars)")
            
            if response_data.get('thinking'):
                thinking_text = response_data['thinking']
                print(f"DEBUG: Got thinking field ({len(thinking_text)} chars)")
            
            # If we have thinking but no response, extract JSON from thinking
            if thinking_text and not generated_text:
                # Look for JSON object in thinking
                import re
                # Find JSON-like structures
                json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                matches = list(re.finditer(json_pattern, thinking_text, re.DOTALL))
                
                if matches:
                    # Try the largest match first (likely the complete JSON)
                    matches.sort(key=lambda m: len(m.group()), reverse=True)
                    for match in matches:
                        potential_json = match.group()
                        try:
                            # Try to parse it
                            test = json.loads(potential_json)
                            if 'summary' in test or 'differential' in test:
                                generated_text = potential_json
                                print(f"DEBUG: Extracted valid JSON from thinking ({len(generated_text)} chars)")
                                break
                        except:
                            continue
                
                if not generated_text:
                    # Fallback: use full thinking
                    generated_text = thinking_text
                    print("DEBUG: Using full thinking field as fallback")
            
            if not generated_text:
                print("WARNING: Empty response from Ollama")
                print(f"Full response data: {str(response_data)[:500]}")
                raise Exception("Empty response from Ollama API")
            
            # Try to extract JSON from response
            # Sometimes models wrap JSON in markdown code blocks
            generated_text = generated_text.strip()
            if '```json' in generated_text:
                generated_text = generated_text.split('```json')[1].split('```')[0].strip()
            elif '```' in generated_text:
                generated_text = generated_text.split('```')[1].split('```')[0].strip()
            
            # Parse response
            result = json.loads(generated_text)
            
            # Add metadata
            if "model_metadata" not in result:
                result["model_metadata"] = {}
            
            cost_info = "Ollama Cloud (cheap!)" if self.is_cloud else "FREE (local)"
            result["model_metadata"].update({
                "llm_model": self.model,
                "embedding_model": config.LOCAL_EMBEDDING_MODEL,
                "retrieval_k": len(chunks),
                "cost": cost_info
            })
            
            if patient_id and not result.get("patient_id"):
                result["patient_id"] = patient_id
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response: {generated_text[:500]}...")
            return {
                "error": "Failed to parse LLM response",
                "patient_id": patient_id,
                "summary": {"text": [], "supporting_evidence": []},
                "differential": [],
                "warnings": [f"JSON parsing error: {str(e)}. Try using a different model or adjusting the prompt."],
                "model_metadata": {
                    "llm_model": self.model,
                    "embedding_model": config.LOCAL_EMBEDDING_MODEL,
                    "retrieval_k": len(chunks),
                    "cost": "FREE"
                }
            }
        except Exception as e:
            print(f"Error generating output: {e}")
            return {
                "error": str(e),
                "patient_id": patient_id,
                "summary": {"text": [], "supporting_evidence": []},
                "differential": [],
                "warnings": [f"Generation error: {str(e)}"],
                "model_metadata": {
                    "llm_model": self.model,
                    "embedding_model": config.LOCAL_EMBEDDING_MODEL,
                    "retrieval_k": len(chunks),
                    "cost": "FREE"
                }
            }


if __name__ == "__main__":
    # Test the generator
    sample_chunks = [
        {
            "chunk_id": "chunk_1",
            "section": "HPI",
            "text": "Mr. Sharma, 65-year-old male, presents with fever (38.9°C), productive cough, and shortness of breath for 3 days."
        },
        {
            "chunk_id": "chunk_2",
            "section": "Imaging",
            "text": "Chest X-ray shows right lower lobe consolidation consistent with lobar pneumonia."
        },
        {
            "chunk_id": "chunk_3",
            "section": "Labs",
            "text": "WBC 16.5 x10^9/L (elevated), CRP 120 mg/L (elevated)."
        }
    ]
    
    generator = ClinicalGenerator()
    result = generator.generate_clinical_output(sample_chunks, patient_id="PT001")
    
    print("\nGenerated Output:")
    print(json.dumps(result, indent=2))
