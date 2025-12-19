<<<<<<< HEAD
# Codex-AIT-Pune
This repository contains our AI-MlL model Project.
=======
# inter-iiit
<<<<<<< HEAD
# my-project
=======
# Clinical RAG System �

**AI-Powered Clinical Note Summarization and Differential Diagnosis Generator**

A Retrieval-Augmented Generation (RAG) system that processes unstructured clinical notes to generate:
1. **Concise, factual summaries** of patient conditions
2. **Prioritized differential diagnoses** with evidence-based citations

## ⚡ Quick Start

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd clinical-rag-system

# 2. Run the automated setup script
chmod +x SETUP.sh  # Make it executable (first time only)
./SETUP.sh

# 3. Get your FREE Ollama API key
# Visit: https://ollama.com/settings/keys

# 4. Configure your environment
cp .env.example .env  # If not already done by SETUP.sh
nano .env  # or use any text editor (vim, code, etc.)
# Change: OLLAMA_API_KEY=your_actual_key_here

# 5. Verify everything is working (OPTIONAL but recommended)
python3 preflight_check.py

# 6. Activate virtual environment (created by SETUP.sh)
source venv/bin/activate

# 7. Run the demo!
python3 main.py --demo

# 8. Try different cases
python3 main.py --list-cases
python3 main.py --demo --case mi_case
```

**That's it!** The setup script handles everything:
- ✅ Creates virtual environment
- ✅ Installs all dependencies
- ✅ Creates `.env` from `.env.example`
- ✅ Downloads embedding models
- ✅ Runs system checks

## 💰 Cost & Privacy

- **LLM**: Ollama Cloud - Very cheap pay-per-use (~$0.001/note)
- **Embeddings**: sentence-transformers - FREE (runs locally)
- **Vector DB**: ChromaDB - FREE (runs locally)
- **Privacy**: Medical data processed locally, only text sent to Ollama
- **No GPU needed**: Cloud-based inference

## 🎯 Problem Statement

Develop a Generative AI system that processes large, unstructured clinical notes and generates two key outputs: a concise, factual summary of the patient's condition and a prioritized list of potential differential diagnoses. The model uses LLMs augmented via Retrieval-Augmented Generation (RAG) to ensure accuracy and traceability, referencing specific parts of the input text to justify each diagnosis. This solution aims to reduce clinician workload, minimize diagnostic errors, and enhance decision-making in healthcare.

## ✨ Features

- **Intelligent Chunking**: Automatically segments clinical notes by sections (HPI, Labs, Imaging, etc.)
- **Vector-based Retrieval**: Uses embeddings and ChromaDB for semantic search
- **Local LLM Generation**: Produces structured JSON output with Ollama (Llama 3.2)
- **Free Embeddings**: sentence-transformers for zero-cost vector embeddings
- **Evidence Tracing**: Every diagnosis includes citations with exact text offsets
- **Confidence Scoring**: Each diagnosis has a confidence score (0.0-1.0)
- **Conservative Approach**: States "insufficient evidence" rather than guessing

## 🏗️ Architecture

```
Clinical Note (Text)
        ↓
   [Chunker] → Chunks with metadata (section, chunk_id)
        ↓
   [Embedder] → Vector embeddings (sentence-transformers: all-MiniLM-L6-v2)
        ↓
   [ChromaDB] → Vector storage & retrieval
        ↓
   [Retriever] → Top-K relevant chunks (K=10)
        ↓
   [Generator] → LLM (Ollama: llama3.2, temp=0.0)
        ↓
   Structured JSON Output
   ├── Summary (with evidence)
   ├── Differential Diagnoses (ranked, with confidence)
   └── Metadata
```

## 📦 Installation

### Prerequisites
- Python 3.8+
- Ollama installed on your system

### Quick Setup

1. **Install Ollama** (if not already installed):
```bash
# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Download from https://ollama.com/download
```

2. **Pull the LLM model**:
```bash
ollama pull llama3.2
```

3. **Clone or download this repository**

4. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

5. **Configure settings** (optional):
The `.env` file is already configured for FREE usage. You can modify settings if needed:
```env
OLLAMA_MODEL=llama3.2
LOCAL_EMBEDDING_MODEL=all-MiniLM-L6-v2
RETRIEVAL_K=10
```

## 🚀 Quick Start

### 1. Start Ollama Server
```bash
ollama serve
```

### 2. Run Demo with Sample Cases

```bash
# Run with default pneumonia case
python main.py --demo

# Run with myocardial infarction case
python main.py --demo --case mi_case

# Run with sepsis case
python main.py --demo --case sepsis_case

# List all available cases
python main.py --list-cases
```

### Analyze Custom Clinical Notes

```bash
# Analyze your own clinical note
python main.py --file path/to/your/note.txt --patient-id PT123 --output results.json
```

## 📝 Sample Cases Included

1. **pneumonia_case**: Community-acquired pneumonia with fever, cough, and consolidation
2. **mi_case**: Acute ST-elevation myocardial infarction (STEMI)
3. **sepsis_case**: Urosepsis with septic shock in patient with indwelling catheter

## 🔧 Configuration

Edit `.env` to customize:

- **OLLAMA_MODEL**: Default is `llama3.2` (you can also use `mistral`, `llama2`, etc.)
- **LOCAL_EMBEDDING_MODEL**: Default is `all-MiniLM-L6-v2` (sentence-transformers)
- **TEMPERATURE**: Set to 0.0 for deterministic outputs
- **RETRIEVAL_K**: Number of chunks to retrieve (10 recommended)
- **CHUNK_SIZE**: Maximum tokens per chunk (512 default)
- **OLLAMA_BASE_URL**: Ollama server URL (default: `http://localhost:11434`)

## 📊 Output Format

The system generates structured JSON output:

```json
{
  "patient_id": "PT001",
  "summary": {
    "text": [
      "65-year-old male presenting with fever, productive cough, and dyspnea for 3 days.",
      "Vital signs show fever (38.9°C), tachypnea (24/min), and hypoxia (SpO2 91%).",
      "..."
    ],
    "supporting_evidence": [
      {
        "chunk_id": "chunk_1",
        "offset": [0, 95],
        "quote": "Mr. Sharma, 65-year-old male, presents with fever..."
      }
    ]
  },
  "differential": [
    {
      "rank": 1,
      "diagnosis": "Community-Acquired Pneumonia",
      "confidence": 0.95,
      "rationale": "Right lower lobe consolidation on CXR with fever, productive cough, elevated WBC and inflammatory markers",
      "supporting_evidence": [
        {
          "chunk_id": "chunk_2",
          "offset": [0, 78],
          "quote": "Chest X-ray shows right lower lobe consolidation consistent with lobar pneumonia"
        }
      ],
      "evidence_score": 0.92
    }
  ],
  "warnings": [],
  "model_metadata": {
    "llm_model": "llama3.2",
    "embedding_model": "all-MiniLM-L6-v2",
    "retrieval_k": 10
  }
}
```

## 🧪 Testing Individual Modules

Each module can be tested independently:

```bash
# Test chunker
python chunker.py

# Test retriever
python retriever.py

# Test generator
python generator.py

# Test full pipeline
python pipeline.py
```

## 📚 Module Overview

### `chunker.py`
- Segments clinical notes by sections (HPI, Labs, Imaging, etc.)
- Creates overlapping chunks for better context
- Adds metadata (chunk_id, section, patient_id)

### `retriever.py`
- Manages ChromaDB vector database
- Generates embeddings via sentence-transformers (local)
- Retrieves top-K most relevant chunks

### `generator.py`
- Formats chunks into prompts
- Calls Ollama LLM to generate structured JSON
- Includes verification/scoring capabilities

### `pipeline.py`
- Orchestrates end-to-end workflow
- Combines chunking → retrieval → generation
- Provides high-level API

### `main.py`
- CLI interface for users
- Demo mode with sample cases
- Custom file analysis

## 🔬 Advanced Usage

### Using the Pipeline Programmatically

```python
from pipeline import ClinicalRAGPipeline

# Initialize
pipeline = ClinicalRAGPipeline()
pipeline.initialize_collection()

# Analyze a note
result = pipeline.analyze_note(
    note="Chief Complaint: ...",
    patient_id="PT001"
)

# Access results
for dx in result['differential']:
    print(f"{dx['diagnosis']}: {dx['confidence']}")
```

### Batch Processing Multiple Notes

```python
from pipeline import ClinicalRAGPipeline

pipeline = ClinicalRAGPipeline()
pipeline.initialize_collection()

notes = [
    ("PT001", note1_text),
    ("PT002", note2_text),
    # ...
]

results = []
for patient_id, note in notes:
    result = pipeline.analyze_note(note, patient_id)
    results.append(result)
```

## 🎓 Prompts Reference

The system uses carefully crafted prompts:

1. **System Prompt**: Conservative, evidence-only instructions
2. **Retrieval Query**: Guides semantic search for relevant chunks
3. **Generation Prompt**: Specifies exact JSON schema and requirements
4. **Verification Prompt**: Scores evidence support (0.0-1.0)

All prompts are defined in `config.py` and follow the specifications from your original prompt document.

## ⚙️ Requirements

- Python 3.8+
- Ollama installed and running
- Required packages (see `requirements.txt`)

## 🔒 Privacy & Security

- **100% Local Processing**: All clinical notes are processed on your machine
- **No External APIs**: Zero data sent to external services
- **Local Storage**: Vector database stored locally in `./chroma_db`
- **Complete Privacy**: Your data never leaves your computer
- **HIPAA-Friendly**: Can be deployed in secure, air-gapped environments

## 🤝 Contributing

This is a prototype/demo system built with 100% FREE local models. For production use, consider:
- Enhanced security and audit logging
- Clinical validation by licensed professionals
- Integration with EHR systems
- Multi-model support and fine-tuning

## 📄 License

This is a demonstration system for educational purposes.

## ⚠️ Disclaimer

**This system is for demonstration and research purposes only. It is NOT approved for clinical use. All clinical decisions must be made by qualified healthcare professionals. Do not use this system for actual patient care without proper validation, regulatory approval, and oversight.**

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. "No module named 'dotenv'" or similar import errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. "OLLAMA_API_KEY not found" or authentication errors
```bash
# Check if .env file exists
ls -la .env

# If missing, copy from example
cp .env.example .env

# Edit and add your API key
nano .env
# Set: OLLAMA_API_KEY=your_actual_api_key_here
```

#### 3. Ollama connection errors (local setup)
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start Ollama
ollama serve

# Verify model is installed
ollama list
ollama pull llama3.2  # If not installed
```

#### 4. "ChromaDB" or database errors
```bash
# Remove corrupted database
rm -rf chroma_db/

# Re-run the program (it will recreate)
python3 main.py --demo
```

#### 5. Python version issues
```bash
# Check Python version (needs 3.8+)
python3 --version

# If too old, install newer Python or use conda
```

#### 6. Permission denied when running SETUP.sh
```bash
# Make script executable
chmod +x SETUP.sh

# Run again
./SETUP.sh
```

#### 7. Out of memory errors
- Reduce `CHUNK_SIZE` in `.env` (try 256 instead of 512)
- Reduce `RETRIEVAL_K` (try 5 instead of 10)
- Use a smaller embedding model

#### 8. Slow performance
- **For Ollama Cloud**: Check your internet connection
- **For Local Ollama**: Use a smaller model (`ollama pull llama3.2:latest`)
- Reduce `MAX_TOKENS` in `.env`

### Getting Help

If you encounter other issues:
1. Check the terminal output for specific error messages
2. Verify all dependencies are installed: `pip list`
3. Ensure your `.env` file is properly configured
4. Try running the test suite: `python3 test_system.py`
5. Check the [Ollama documentation](https://ollama.com/docs)

---

## 🎯 Getting Started Checklist

- [ ] Clone the repository from GitHub
- [ ] Run setup script: `chmod +x SETUP.sh && ./SETUP.sh`
- [ ] Copy environment template: `cp .env.example .env` (if not done automatically)
- [ ] Get Ollama API key from: https://ollama.com/settings/keys
- [ ] Edit `.env` and add your API key: `OLLAMA_API_KEY=your_key_here`
- [ ] Activate virtual environment: `source venv/bin/activate`
- [ ] Run tests: `python3 test_system.py`
- [ ] Run demo: `python3 main.py --demo`
- [ ] Review output JSON file: `output_pneumonia_case.json`
- [ ] Try other sample cases: `python3 main.py --list-cases`
- [ ] Experiment with your own notes: `python3 main.py --file your_note.txt`

## 💡 Tips

1. **Temperature=0.0** ensures deterministic outputs
2. **K=10** balances context vs. noise for retrieval
3. Review `supporting_evidence` to verify claims
4. Check `warnings` field for insufficient evidence flags
5. Adjust `CHUNK_SIZE` for different note lengths
6. Try different Ollama models: `ollama pull mistral` then update `.env`

## 🆓 Cost Breakdown

| Component | FREE Version | Notes |
|-----------|--------------|-------|
| LLM (Generation) | $0.00 | Ollama (local) |
| Embeddings | $0.00 | sentence-transformers (local) |
| Vector DB | $0.00 | ChromaDB (local) |
| Storage | $0.00 | Your disk space |
| **TOTAL** | **$0.00 forever** | ✅ |

---

**Built with ❤️ for improving clinical decision support**
>>>>>>> 82c69ec (feat: Clinical RAG System - GitHub ready version)
>>>>>>> 0a2d468 (Initial project upload)
"# Team--Codex-AIT-Pune" 
