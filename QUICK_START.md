# First Time Setup - Quick Guide

## For Users Cloning from GitHub

Follow these steps to get the Clinical RAG System running on your machine:

### ✅ Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd clinical-rag-system
```

### ✅ Step 2: Run the Setup Script
```bash
# Make it executable (first time only)
chmod +x SETUP.sh

# Run the setup
./SETUP.sh
```

This will:
- ✅ Create a Python virtual environment
- ✅ Install all required packages
- ✅ Create a `.env` file from `.env.example`
- ✅ Run pre-flight checks

### ✅ Step 3: Get Your Ollama API Key

#### Option A: Ollama Cloud (Recommended - No GPU needed!)
1. Go to: https://ollama.com/settings/keys
2. Create a FREE account if you don't have one
3. Generate an API key
4. Copy the key

#### Option B: Local Ollama (If you prefer running locally)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama
ollama serve

# Pull the model
ollama pull llama3.2
```

### ✅ Step 4: Configure Your Environment

1. **Open the `.env` file** (created by SETUP.sh):
   ```bash
   nano .env
   # or
   code .env
   # or use any text editor
   ```

2. **For Ollama Cloud**, update these lines:
   ```env
   OLLAMA_BASE_URL=https://ollama.com
   OLLAMA_API_KEY=your_actual_api_key_here  # ← Paste your key here
   OLLAMA_MODEL=gpt-oss:20b
   ```

3. **For Local Ollama**, update these lines:
   ```env
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_API_KEY=  # ← Leave empty for local
   OLLAMA_MODEL=llama3.2
   ```

4. **Save and close** the file

### ✅ Step 5: Verify Setup (Optional but Recommended)
```bash
python3 preflight_check.py
```

This will check:
- ✅ Python version
- ✅ All dependencies installed
- ✅ Project files present
- ✅ `.env` configuration
- ✅ Ollama connection

### ✅ Step 6: Activate Virtual Environment
```bash
source venv/bin/activate
```

You'll see `(venv)` in your terminal prompt.

### ✅ Step 7: Run the Demo!
```bash
python3 main.py --demo
```

You should see:
- System initialization
- Chunking progress
- Embedding progress
- Generation output
- JSON results saved to `output_pneumonia_case.json`

### ✅ Step 8: Explore More

```bash
# List all available sample cases
python3 main.py --list-cases

# Try other cases
python3 main.py --demo --case mi_case
python3 main.py --demo --case sepsis_case

# Analyze your own clinical note
python3 main.py --file your_note.txt --patient-id PT001
```

---

## 🚨 Common Issues

### "No module named 'dotenv'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Cannot connect to Ollama"
- **Cloud**: Check your API key in `.env`
- **Local**: Make sure Ollama is running: `ollama serve`

### "Permission denied: ./SETUP.sh"
```bash
chmod +x SETUP.sh
```

### Need Help?
- Check the full [README.md](README.md)
- See [Troubleshooting](README.md#-troubleshooting) section
- Open a GitHub Issue

---

## 💰 Cost

- **Ollama Cloud**: Very cheap pay-per-use (~$0.001 per note)
- **Local Ollama**: Completely FREE
- **Embeddings**: FREE (runs locally)
- **Vector DB**: FREE (runs locally)

## 🔐 Privacy

- All embeddings run locally (FREE)
- Clinical notes processed on your machine
- Only text sent to Ollama (if using cloud)
- No data sharing with third parties

---

**You're all set! Happy analyzing! 🏥**
