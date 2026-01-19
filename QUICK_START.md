# ⚡ Quick Start Guide

Get your Second Brain AI up and running in 5 minutes!

## Prerequisites Check

Open Terminal and verify:

```bash
# Check Python (need 3.9+)
python3 --version

# Check if Homebrew is installed
brew --version
```

If any are missing, see SETUP_GUIDE.md for installation.

## Installation (Choose One Method)

### Method 1: Automated Setup (Recommended)

```bash
cd second-brain-ai
chmod +x setup.sh
./setup.sh
```

This will:
- Create virtual environment
- Install all dependencies
- Download the Llama2 model

### Method 2: Manual Setup

```bash
cd second-brain-ai

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Ollama
brew install ollama

# Download LLM model
ollama pull llama2
```

## Running the App

**Terminal 1 - Start Ollama:**
```bash
ollama serve
```
Leave this running.

**Terminal 2 - Start App:**
```bash
cd second-brain-ai
source venv/bin/activate
streamlit run app.py
```

The app opens at: http://localhost:8501

## First Steps

1. **Upload a document**: Click "Browse files" → Select `sample_document.txt` → Click "Add to Knowledge Base"

2. **Ask a question**: Type "What is RAG?" → Click "Search Knowledge Base"

3. **View sources**: Click "View Sources" to see where the answer came from

## Daily Workflow

```bash
# Terminal 1
ollama serve

# Terminal 2
cd second-brain-ai
source venv/bin/activate
streamlit run app.py
```

## Troubleshooting

**"Connection refused"**
→ Make sure Ollama is running: `ollama serve`

**"No module named 'streamlit'"**
→ Activate virtual environment: `source venv/bin/activate`

**"Model not found"**
→ Download model: `ollama pull llama2`

## Next Steps

- Upload your PDFs, notes, and documents
- Try asking complex questions
- Experiment with different LLM models (mistral, codellama)
- Read SETUP_GUIDE.md for advanced usage

## Need Help?

1. Check SETUP_GUIDE.md for detailed instructions
2. Review error messages in Terminal
3. Check GitHub Issues for common problems

---

Happy querying! 🧠✨
