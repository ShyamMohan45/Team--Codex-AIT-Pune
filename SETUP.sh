#!/bin/bash

# Clinical RAG System - Complete Setup Script
# Works with Ollama Cloud (no local GPU needed!)

echo "=========================================================="
echo "🏥 Clinical RAG System - Complete Setup"
echo "=========================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check Python version
echo "1. Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
echo ""
echo "2. Creating virtual environment..."
if [ -d "venv" ]; then
    print_info "Virtual environment already exists"
else
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        print_success "Virtual environment created"
    else
        print_error "Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo ""
echo "3. Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
echo ""
echo "4. Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "pip upgraded"

# Install dependencies
echo ""
echo "5. Installing Python dependencies..."
echo "   This may take a few minutes..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    print_success "All dependencies installed"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Create .env file if it doesn't exist
echo ""
echo "6. Setting up configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success ".env file created from .env.example"
        print_info "IMPORTANT: Edit .env and add your Ollama API key!"
    else
        print_error ".env.example not found! Creating basic .env file..."
        cat > .env << 'EOF'
# Ollama Cloud Configuration
# Get your free API key at: https://ollama.com/settings/keys

# Ollama Cloud settings
OLLAMA_BASE_URL=https://ollama.com
OLLAMA_API_KEY=your_api_key_here
OLLAMA_MODEL=gpt-oss:20b

# Local embedding model (FREE - runs on your machine)
LOCAL_EMBEDDING_MODEL=all-MiniLM-L6-v2

# General settings
TEMPERATURE=0.0
MAX_TOKENS=1200
RETRIEVAL_K=10
CHUNK_SIZE=512
CHUNK_OVERLAP=50
EOF
        print_success ".env file created"
        print_info "IMPORTANT: Edit .env and add your Ollama API key!"
    fi
else
    print_info ".env file already exists (not overwriting)"
fi

# Run tests
echo ""
echo "7. Running pre-flight checks..."
python3 preflight_check.py
PREFLIGHT_RESULT=$?

# Summary
echo ""
echo "=========================================================="
if [ $PREFLIGHT_RESULT -eq 0 ]; then
    print_success "Setup Complete - All Systems Ready!"
else
    print_error "Setup completed with warnings - Please review above"
fi
echo "=========================================================="
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Get your FREE Ollama Cloud API key:"
echo "   https://ollama.com/settings/keys"
echo ""
echo "2. Edit .env file and add your API key:"
echo "   OLLAMA_API_KEY=your_actual_key_here"
echo ""
echo "3. Activate virtual environment (every time you use this):"
echo "   source venv/bin/activate"
echo ""
echo "4. Run the demo:"
echo "   python3 main.py --demo"
echo ""
echo "5. Try other cases:"
echo "   python3 main.py --list-cases"
echo "   python3 main.py --demo --case mi_case"
echo ""
echo "💰 Cost: Ollama Cloud is very cheap (pay-per-use)"
echo "🔒 Privacy: Embeddings run locally (FREE)"
echo ""
echo "For more help, see README.md"
echo ""
