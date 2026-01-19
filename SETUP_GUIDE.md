# 🍎 Complete Setup Guide for Mac

This guide will walk you through setting up the Second Brain AI project on your Mac from scratch.

## Prerequisites

Before you begin, make sure you have:
- macOS 10.15 (Catalina) or later
- Admin access to your Mac
- At least 8GB of RAM
- 5GB of free disk space

## Step-by-Step Installation

### 1. Install Homebrew (if not already installed)

Homebrew is a package manager for Mac. Open Terminal and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the on-screen instructions. After installation, you may need to add Homebrew to your PATH:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### 2. Install Python 3

Check if Python 3 is already installed:

```bash
python3 --version
```

If not installed or version is below 3.9, install it:

```bash
brew install python@3.11
```

Verify installation:

```bash
python3 --version
# Should show Python 3.11.x or higher
```

### 3. Install Ollama

Ollama is required for running the local LLM. Install it using Homebrew:

```bash
brew install ollama
```

Or download from [https://ollama.ai](https://ollama.ai)

### 4. Clone or Download the Project

If you have the project folder:
```bash
cd ~/Downloads  # or wherever you downloaded it
```

If cloning from GitHub:
```bash
cd ~
git clone https://github.com/yourusername/second-brain-ai.git
cd second-brain-ai
```

### 5. Run the Automated Setup Script

We've created a script to automate the setup process:

```bash
chmod +x setup.sh
./setup.sh
```

This script will:
- Create a virtual environment
- Install all Python dependencies
- Download the Llama2 model

**Note**: The model download may take 5-10 minutes depending on your internet speed.

### 6. Manual Setup (Alternative to Step 5)

If you prefer to set up manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download LLM model
ollama pull llama2
```

## Running the Application

### Starting Ollama Service

Open a new Terminal window and start Ollama:

```bash
ollama serve
```

Keep this terminal window open while using the app.

### Starting the Second Brain AI

In another Terminal window:

```bash
# Navigate to project directory
cd ~/second-brain-ai  # adjust path as needed

# Activate virtual environment
source venv/bin/activate

# Run the application
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

## First Time Usage

1. **Upload a Document**:
   - Click "Browse files" in the sidebar
   - Select a PDF, TXT, or DOCX file
   - Click "Add to Knowledge Base"
   - Wait for processing (you'll see a success message)

2. **Ask a Question**:
   - Type your question in the main text area
   - Click "Search Knowledge Base"
   - View the AI-generated answer

3. **Try the Sample Document**:
   - Upload the included `sample_document.txt`
   - Ask: "What is RAG and how does it work?"
   - See the AI retrieve and answer from the document

## Troubleshooting

### Issue: "command not found: python3"
**Solution**: Install Python using Homebrew:
```bash
brew install python@3.11
```

### Issue: "Connection refused" when querying
**Solution**: Make sure Ollama is running:
```bash
ollama serve
```

### Issue: "No module named 'streamlit'"
**Solution**: Activate the virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Ollama model not found
**Solution**: Download the model:
```bash
ollama pull llama2
```

Check available models:
```bash
ollama list
```

### Issue: Application is slow
**Solutions**:
- Use a smaller model (mistral is faster than llama2)
- Close other applications to free up RAM
- Reduce chunk size in app.py (line 35)

### Issue: Port 8501 already in use
**Solution**: Kill the existing Streamlit process:
```bash
pkill -f streamlit
streamlit run app.py
```

Or use a different port:
```bash
streamlit run app.py --server.port 8502
```

## Daily Usage Workflow

Each time you want to use the app:

1. Open Terminal
2. Start Ollama: `ollama serve` (in one window)
3. In a new Terminal window:
   ```bash
   cd ~/second-brain-ai
   source venv/bin/activate
   streamlit run app.py
   ```

## Stopping the Application

1. In the Streamlit terminal: Press `Ctrl + C`
2. In the Ollama terminal: Press `Ctrl + C`
3. Deactivate virtual environment: `deactivate`

## Updating the Application

If you make changes to the code:

```bash
# Stop the running app (Ctrl + C)
# Restart it
streamlit run app.py
```

If you add new dependencies:

```bash
pip install -r requirements.txt
```

## Uninstalling

To completely remove the application:

```bash
# Remove the project folder
rm -rf ~/second-brain-ai

# Optionally remove Ollama
brew uninstall ollama

# Remove downloaded models (optional)
rm -rf ~/.ollama
```

## Additional Tips

### Using Different Models

Download other models:
```bash
ollama pull mistral    # Faster, good quality
ollama pull codellama  # Better for code-related queries
```

Select them in the app's Settings dropdown.

### Keyboard Shortcuts

- **⌘ + R**: Refresh the app
- **⌘ + W**: Close the browser tab
- **Ctrl + C**: Stop the server

### Performance Optimization

For better performance on older Macs:
1. Use the Mistral model (faster than Llama2)
2. Close unnecessary applications
3. Reduce `chunk_size` in app.py
4. Upload smaller documents initially

## Getting Help

If you encounter issues:
1. Check the Troubleshooting section above
2. Review error messages in the Terminal
3. Ensure all prerequisites are met
4. Try restarting both Ollama and the app

## Next Steps

- Upload your personal documents
- Experiment with different questions
- Try different LLM models
- Customize the code to fit your needs
- Share your improvements on GitHub

---

Happy knowledge building! 🧠✨
