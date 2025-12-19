# Contributing to Clinical RAG System

Thank you for your interest in contributing! This project welcomes contributions of all kinds.

## 🚀 Quick Start for Contributors

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/clinical-rag-system.git
   cd clinical-rag-system
   ```
3. **Run the setup**:
   ```bash
   ./SETUP.sh
   ```
4. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🛠️ Development Setup

```bash
# Activate virtual environment
source venv/bin/activate

# Install development dependencies (if any)
pip install -r requirements.txt

# Run tests before making changes
python3 test_system.py
```

## 📝 Types of Contributions

### 1. Bug Reports
- Use GitHub Issues
- Include error messages, steps to reproduce
- Specify your OS, Python version, and Ollama version

### 2. Feature Requests
- Open a GitHub Issue with the "enhancement" label
- Describe the use case and expected behavior

### 3. Code Contributions
- Fix bugs
- Add new features
- Improve documentation
- Add test cases
- Optimize performance

### 4. Sample Clinical Notes
- Add more diverse clinical cases to `sample_notes.py`
- Ensure patient data is completely de-identified/synthetic

## 🔍 Code Standards

- **Python Style**: Follow PEP 8
- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Include where appropriate
- **Comments**: Explain "why", not "what"

## ✅ Pull Request Process

1. **Test your changes**:
   ```bash
   python3 test_system.py
   python3 main.py --demo --case pneumonia_case
   python3 main.py --demo --case mi_case
   ```

2. **Update documentation** if needed:
   - README.md for user-facing changes
   - Docstrings for code changes
   - CHANGELOG.md for version updates

3. **Create a Pull Request**:
   - Clear title and description
   - Reference any related issues
   - List what was changed and why

4. **Code Review**:
   - Address reviewer feedback
   - Keep commits clean and focused

## 🧪 Testing Guidelines

- Test with all sample cases
- Verify output JSON is valid
- Check that evidence citations are accurate
- Test edge cases (empty notes, malformed input, etc.)

## 🔐 Security & Privacy

- **Never commit real patient data**
- **Never commit API keys** (use .env.example as template)
- All sample data must be synthetic/de-identified
- Follow HIPAA guidelines for healthcare data

## 📋 Checklist Before Submitting PR

- [ ] Code runs without errors
- [ ] All tests pass (`python3 test_system.py`)
- [ ] Demo works with sample cases
- [ ] Documentation updated if needed
- [ ] No real patient data or API keys committed
- [ ] Code follows project style
- [ ] Commits have clear messages

## 💬 Questions?

Open a GitHub Issue with the "question" label, and we'll help you out!

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as this project.

---

Thank you for helping improve clinical decision support! 🙏
