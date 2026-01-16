#!/bin/bash

# Second Brain AI Setup Script
# This script automates the setup process for the Second Brain AI project

set -e

echo "🧠 Second Brain AI - Setup Script"
echo "=================================="
echo ""

# Check Python version
echo "📌 Checking Python version..."
python3 --version

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✅ Virtual environment created!"
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo ""
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed successfully!"

# Check if Ollama is installed
echo ""
echo "📌 Checking for Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama is not installed."
    echo ""
    echo "To install Ollama on macOS:"
    echo "  1. Visit https://ollama.ai"
    echo "  2. Download and install"
    echo "  3. Or use: brew install ollama"
    echo ""
    echo "After installing Ollama, run:"
    echo "  ollama serve        # Start Ollama service"
    echo "  ollama pull llama2  # Download the LLM model"
else
    echo "✅ Ollama is installed!"
    echo ""
    echo "📥 Downloading Llama2 model (this may take a few minutes)..."
    ollama pull llama2
    echo "✅ Llama2 model downloaded!"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Make sure Ollama is running: ollama serve"
echo "  3. Start the app: streamlit run app.py"
echo ""
echo "Happy coding! 🚀"
