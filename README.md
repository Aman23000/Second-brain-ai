# 🧠 Second Brain AI - Personal AI Knowledge Base

A powerful RAG (Retrieval Augmented Generation) application that transforms your documents into an intelligent, queryable knowledge base. Upload PDFs, notes, and documents, then ask questions as if you're querying your own brain.

## 🌟 Features

- **Multi-Format Support**: Upload PDF, TXT, and DOCX files
- **Intelligent Chunking**: Automatic document processing with smart text splitting
- **Vector Search**: Powered by ChromaDB and sentence transformers
- **Local LLM Integration**: Uses Ollama for privacy-focused, local AI inference
- **Interactive UI**: Beautiful Streamlit interface for easy interaction
- **Source Attribution**: See which documents your answers come from
- **Persistent Storage**: Your knowledge base is saved and grows over time

## 🏗️ Architecture

The project uses a modern RAG architecture:

1. **Document Processing Pipeline**
   - Multi-format loaders (PDF, DOCX, TXT)
   - Recursive character text splitter for optimal chunking
   - Metadata preservation for source tracking

2. **Embedding & Vector Storage**
   - Sentence Transformers (all-MiniLM-L6-v2) for embeddings
   - ChromaDB for efficient vector storage and retrieval
   - Persistent database for maintaining knowledge across sessions

3. **Retrieval & Generation**
   - Semantic similarity search for relevant context retrieval
   - LangChain RetrievalQA for orchestration
   - Ollama for local LLM inference

## 📋 Prerequisites

Before you begin, ensure you have:

- Python 3.9 or higher
- Ollama installed (for local LLM inference)
- At least 8GB RAM (16GB recommended)
- 5GB free disk space

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/second-brain-ai.git
cd second-brain-ai
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Ollama

**On macOS:**
```bash
# Download and install from https://ollama.ai
# Or using Homebrew:
brew install ollama

# Start Ollama service
ollama serve
```

**On Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
```

### Step 5: Download LLM Model

In a new terminal:
```bash
# Download the default model (llama2)
ollama pull llama2

# Optional: Download other models
ollama pull mistral
ollama pull codellama
```

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 💻 Usage

### Adding Documents

1. Click the **"Browse files"** button in the sidebar
2. Select your PDF, TXT, or DOCX file
3. Click **"Add to Knowledge Base"**
4. Wait for processing to complete

### Querying Your Knowledge Base

1. Type your question in the main text area
2. Click **"Search Knowledge Base"**
3. View the AI-generated answer
4. Expand "View Sources" to see relevant document excerpts

### Tips for Best Results

- **Be specific**: "What are the key findings from the Q4 report?" works better than "Tell me about Q4"
- **Upload related documents**: The more context, the better the answers
- **Try different models**: Mistral might give different insights than Llama2
- **Check sources**: Always verify important information from the source documents

## 📁 Project Structure

```
second-brain-ai/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── chroma_db/             # Vector database (created on first run)
└── .gitignore            # Git ignore file
```

## 🛠️ Technical Stack

- **Framework**: Streamlit (UI)
- **LLM Orchestration**: LangChain
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers
- **LLM**: Ollama (Llama2, Mistral, CodeLlama)
- **Document Processing**: PyPDF, python-docx, docx2txt

## 🔧 Configuration

### Changing Chunk Size

Edit `app.py` line 35-37:

```python
self.text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Adjust this
    chunk_overlap=200,    # Adjust this
    length_function=len,
)
```

### Changing Number of Retrieved Documents

Edit `app.py` line 87:

```python
retriever=self.vectorstore.as_retriever(
    search_kwargs={"k": 4}  # Change this number
),
```

## 🐛 Troubleshooting

### "Connection refused" error
- Make sure Ollama is running: `ollama serve`
- Check if the model is downloaded: `ollama list`

### "No module named 'streamlit'"
- Activate your virtual environment
- Reinstall requirements: `pip install -r requirements.txt`

### Slow performance
- Use a smaller LLM model
- Reduce chunk size
- Reduce the number of retrieved documents

### Documents not being added
- Check file format (PDF, TXT, DOCX only)
- Ensure file is not corrupted
- Check console for error messages

## 🚀 Future Enhancements

- [ ] Support for more file formats (MD, HTML, CSV)
- [ ] Conversation history and chat interface
- [ ] Multi-modal support (images, tables)
- [ ] Export/import knowledge base
- [ ] Advanced filtering and search
- [ ] Document summarization
- [ ] API endpoint for programmatic access

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- LangChain for the excellent RAG framework
- ChromaDB for the vector database
- Ollama for making local LLMs accessible
- Streamlit for the amazing UI framework

## 📧 Contact

Your Name - Aman Jain

Project Link:

---


