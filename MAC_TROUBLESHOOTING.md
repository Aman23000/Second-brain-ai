# 🍎 Mac-Specific Troubleshooting Guide

Common issues Mac users face and how to fix them.

## Permission Issues

### Problem: "Permission denied" when running setup.sh

**Solution**:
```bash
chmod +x setup.sh
./setup.sh
```

### Problem: "Cannot install to /usr/local"

**Solution**: Use virtual environment (already in setup.sh):
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Python Issues

### Problem: "python3: command not found"

**Check if installed**:
```bash
which python3
python3 --version
```

**Install via Homebrew**:
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11
```

**Verify installation**:
```bash
python3 --version
# Should show: Python 3.11.x
```

### Problem: Multiple Python versions conflicting

**Solution**: Use specific Python version:
```bash
# List all Python versions
ls -l /usr/local/bin/python*

# Create venv with specific version
/usr/local/bin/python3.11 -m venv venv
```

## Homebrew Issues

### Problem: "brew: command not found"

**Install Homebrew**:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Add to PATH** (M1/M2 Macs):
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

**Add to PATH** (Intel Macs):
```bash
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/usr/local/bin/brew shellenv)"
```

### Problem: Homebrew installation hangs

**Solution**: Check your internet connection and try:
```bash
brew update
brew doctor
```

## Ollama Issues

### Problem: "ollama: command not found"

**Install Ollama**:
```bash
brew install ollama
```

Or download from: https://ollama.ai

**Verify installation**:
```bash
which ollama
ollama --version
```

### Problem: "Cannot connect to Ollama server"

**Start Ollama**:
```bash
ollama serve
```

Leave this terminal open!

**Check if running**:
```bash
# In another terminal
curl http://localhost:11434/api/version
```

### Problem: "Model not found" error

**Download the model**:
```bash
ollama pull llama2
```

**Check installed models**:
```bash
ollama list
```

### Problem: Ollama service stops unexpectedly

**Solution 1**: Restart with logging:
```bash
ollama serve 2>&1 | tee ollama.log
```

**Solution 2**: Check system resources:
```bash
# Check RAM usage
top -l 1 | grep PhysMem

# Close other applications if RAM is low
```

## Virtual Environment Issues

### Problem: "No module named 'venv'"

**Solution**: Python 3.11+ includes venv, reinstall Python:
```bash
brew reinstall python@3.11
```

### Problem: Virtual environment not activating

**Check current shell**:
```bash
echo $SHELL
```

**For bash**:
```bash
source venv/bin/activate
```

**For zsh** (default on newer Macs):
```bash
source venv/bin/activate
```

**For fish**:
```bash
source venv/bin/activate.fish
```

### Problem: "Command not found" after activating venv

**Solution**: Ensure you're in the project directory:
```bash
cd ~/second-brain-ai
source venv/bin/activate
which python
# Should show: /Users/yourusername/second-brain-ai/venv/bin/python
```

## Port Issues

### Problem: "Port 8501 already in use"

**Find and kill the process**:
```bash
lsof -ti:8501 | xargs kill -9
```

Or use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Problem: "Port 11434 already in use" (Ollama)

**Find and kill the process**:
```bash
lsof -ti:11434 | xargs kill -9
ollama serve
```

## M1/M2 Mac Specific Issues

### Problem: Architecture mismatch errors

**Solution**: Use Rosetta for compatibility:
```bash
arch -x86_64 brew install [package]
```

Or install ARM-native Python:
```bash
brew install python@3.11
```

### Problem: "Bad CPU type in executable"

**Solution**: Reinstall with correct architecture:
```bash
# Uninstall
pip uninstall -y [package-name]

# Reinstall
pip install --no-cache-dir [package-name]
```

## Dependency Installation Issues

### Problem: "Failed building wheel for [package]"

**Install build tools**:
```bash
xcode-select --install
```

**Update pip and setuptools**:
```bash
pip install --upgrade pip setuptools wheel
```

### Problem: SSL certificate errors

**Update certificates**:
```bash
pip install --upgrade certifi
/Applications/Python\ 3.11/Install\ Certificates.command
```

### Problem: ChromaDB installation fails

**Install with no cache**:
```bash
pip install --no-cache-dir chromadb
```

If that fails:
```bash
pip install chromadb --no-deps
pip install -r requirements.txt
```

## File System Issues

### Problem: "Read-only file system"

**Check permissions**:
```bash
ls -la ~/second-brain-ai
```

**Fix permissions**:
```bash
sudo chown -R $(whoami) ~/second-brain-ai
chmod -R u+w ~/second-brain-ai
```

### Problem: Hidden .DS_Store files

**These are normal Mac files, already in .gitignore**:
```bash
find . -name ".DS_Store" -delete
```

### Problem: Case sensitivity issues

**Mac is case-insensitive by default**, but Git is case-sensitive:
```bash
# Be consistent with file names
# "README.md" not "readme.md"
```

## Memory Issues

### Problem: "Killed: 9" or app crashes

**Check available memory**:
```bash
# Check RAM
top -l 1 | grep PhysMem

# Check disk space
df -h
```

**Solutions**:
- Close other applications
- Use a smaller LLM model (mistral instead of llama2)
- Reduce chunk size in app.py
- Restart your Mac

### Problem: ChromaDB using too much memory

**Solution**: Reduce batch size and collection size:
```python
# In app.py, modify the retriever
search_kwargs={"k": 2}  # Instead of 4
```

## Network Issues

### Problem: pip install times out

**Use a different index**:
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

Or increase timeout:
```bash
pip install -r requirements.txt --timeout 300
```

### Problem: Ollama download fails

**Use manual download**:
1. Visit https://ollama.ai/library/llama2
2. Download model manually
3. Use `ollama run` to verify

## Terminal Issues

### Problem: "zsh: command not found" after installation

**Reload shell configuration**:
```bash
source ~/.zprofile
# or
source ~/.zshrc
```

### Problem: Environment variables not persisting

**Add to correct config file**:

For **zsh** (default on macOS Catalina+):
```bash
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

For **bash**:
```bash
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

## IDE-Specific Issues

### Problem: VS Code not recognizing virtual environment

**Solution**:
1. Press `Cmd + Shift + P`
2. Type "Python: Select Interpreter"
3. Choose `./venv/bin/python`

### Problem: PyCharm not finding packages

**Solution**:
1. Go to Settings → Project → Python Interpreter
2. Click gear icon → Add
3. Select "Existing environment"
4. Navigate to `venv/bin/python`

## Git Issues on Mac

### Problem: Git credentials not saving

**Use macOS keychain**:
```bash
git config --global credential.helper osxkeychain
```

### Problem: "xcrun: error: invalid active developer path"

**Install Xcode Command Line Tools**:
```bash
xcode-select --install
```

## Performance Optimization for Mac

### For Intel Macs
```bash
# Use all CPU cores
export OMP_NUM_THREADS=4
```

### For M1/M2 Macs
```bash
# Leverage Apple Silicon
export PYTORCH_ENABLE_MPS_FALLBACK=1
```

### Reduce memory usage
Edit `app.py`:
```python
# Line 35-37, reduce chunk size
chunk_size=500,  # Down from 1000
chunk_overlap=100,  # Down from 200
```

## Complete Reset Procedure

If everything breaks:

```bash
# 1. Stop all processes
pkill -f streamlit
pkill -f ollama

# 2. Remove virtual environment
rm -rf venv

# 3. Clear caches
rm -rf chroma_db
rm -rf __pycache__

# 4. Start fresh
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 5. Reinstall Ollama model
ollama pull llama2

# 6. Test
streamlit run app.py
```

## Getting More Help

### System Information for Bug Reports

Run this and share output when asking for help:

```bash
echo "=== System Info ==="
sw_vers
echo ""
echo "=== Python ==="
python3 --version
which python3
echo ""
echo "=== Pip Packages ==="
pip list | grep -E "streamlit|langchain|chromadb|ollama"
echo ""
echo "=== Ollama ==="
ollama list
echo ""
echo "=== Disk Space ==="
df -h | grep -E "Filesystem|/$"
echo ""
echo "=== Memory ==="
top -l 1 | grep PhysMem
```

### Useful Commands

```bash
# Check what's running on ports
lsof -i :8501
lsof -i :11434

# Monitor system resources
top

# Check Python path
which python3
python3 -c "import sys; print(sys.path)"

# Verify installations
pip check

# Test Ollama connection
curl http://localhost:11434/api/tags
```

## Prevention Tips

✅ **Always use virtual environments**
✅ **Keep macOS and Xcode updated**
✅ **Regular Homebrew maintenance**: `brew update && brew upgrade`
✅ **Check system resources before running**
✅ **Read error messages carefully**
✅ **Test with sample document first**

---

Still stuck? Check:
1. PROJECT_OVERVIEW.md for general help
2. SETUP_GUIDE.md for installation steps
3. GitHub Issues for the project
4. Stack Overflow with your error message

Most issues are solved by:
- Reactivating virtual environment
- Restarting Ollama service
- Checking available RAM/disk space
- Ensuring correct Python version

Good luck! 🍀
