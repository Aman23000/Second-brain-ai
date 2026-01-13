import os
import streamlit as st
from pathlib import Path
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
import tempfile
import shutil


class SecondBrainAI:
    """Main class for the Second Brain AI application."""
    
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Initialize or load the vector store
        if os.path.exists(persist_directory):
            self.vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings
            )
        else:
            self.vectorstore = None
    
    def load_document(self, file_path):
        """Load a document based on its file type."""
        file_extension = Path(file_path).suffix.lower()
        
        loaders = {
            '.pdf': PyPDFLoader,
            '.txt': TextLoader,
            '.docx': Docx2txtLoader,
        }
        
        if file_extension not in loaders:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        loader = loaders[file_extension](file_path)
        documents = loader.load()
        return documents
    
    def process_documents(self, documents):
        """Split documents into chunks."""
        texts = self.text_splitter.split_documents(documents)
        return texts
    
    def add_to_knowledge_base(self, file_path):
        """Add a document to the knowledge base."""
        try:
            # Load and process the document
            documents = self.load_document(file_path)
            texts = self.process_documents(documents)
            
            # Create or update the vector store
            if self.vectorstore is None:
                self.vectorstore = Chroma.from_documents(
                    documents=texts,
                    embedding=self.embeddings,
                    persist_directory=self.persist_directory
                )
            else:
                self.vectorstore.add_documents(texts)
            
            # Persist the changes
            self.vectorstore.persist()
            
            return True, f"Successfully added {Path(file_path).name} to knowledge base"
        except Exception as e:
            return False, f"Error processing document: {str(e)}"
    
    def query_knowledge_base(self, query, llm_model="llama2"):
        """Query the knowledge base with a question."""
        if self.vectorstore is None:
            return "No documents in knowledge base. Please add documents first."
        
        try:
            # Initialize the LLM
            llm = Ollama(model=llm_model, temperature=0.7)
            
            # Create a retrieval QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(
                    search_kwargs={"k": 4}
                ),
                return_source_documents=True
            )
            
            # Get the answer
            result = qa_chain({"query": query})
            
            return result
        except Exception as e:
            return f"Error querying knowledge base: {str(e)}"
    
    def get_stats(self):
        """Get statistics about the knowledge base."""
        if self.vectorstore is None:
            return {"total_documents": 0}
        
        try:
            collection = self.vectorstore._collection
            return {
                "total_documents": collection.count()
            }
        except:
            return {"total_documents": 0}


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Second Brain AI",
        page_icon="🧠",
        layout="wide"
    )
    
    st.title("🧠 Second Brain AI")
    st.markdown("*Your personal AI knowledge base - All your PDFs, notes, docs.*")
    st.markdown("---")
    
    # Initialize the Second Brain AI
    if 'brain' not in st.session_state:
        st.session_state.brain = SecondBrainAI()
    
    # Sidebar for document management
    with st.sidebar:
        st.header("📚 Document Management")
        
        uploaded_file = st.file_uploader(
            "Upload documents",
            type=['pdf', 'txt', 'docx'],
            help="Upload PDF, TXT, or DOCX files"
        )
        
        if uploaded_file is not None:
            if st.button("Add to Knowledge Base"):
                with st.spinner("Processing document..."):
                    # Save the uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Process the document
                    success, message = st.session_state.brain.add_to_knowledge_base(tmp_path)
                    
                    # Clean up
                    os.unlink(tmp_path)
                    
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
        
        st.markdown("---")
        
        # Display stats
        st.subheader("📊 Knowledge Base Stats")
        stats = st.session_state.brain.get_stats()
        st.metric("Total Chunks", stats['total_documents'])
        
        st.markdown("---")
        
        # Settings
        st.subheader("⚙️ Settings")
        llm_model = st.selectbox(
            "LLM Model",
            ["llama2", "mistral", "codellama"],
            help="Select the Ollama model to use"
        )
        st.session_state.llm_model = llm_model
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Ask Questions")
        
        # Query input
        query = st.text_area(
            "What would you like to know?",
            height=100,
            placeholder="Ask anything about your documents..."
        )
        
        if st.button("Search Knowledge Base", type="primary"):
            if query:
                with st.spinner("Searching knowledge base..."):
                    result = st.session_state.brain.query_knowledge_base(
                        query,
                        llm_model=st.session_state.get('llm_model', 'llama2')
                    )
                    
                    if isinstance(result, dict) and 'result' in result:
                        st.markdown("### Answer")
                        st.write(result['result'])
                        
                        if 'source_documents' in result and result['source_documents']:
                            with st.expander("📄 View Sources"):
                                for i, doc in enumerate(result['source_documents'], 1):
                                    st.markdown(f"**Source {i}:**")
                                    st.text(doc.page_content[:300] + "...")
                                    st.markdown("---")
                    else:
                        st.info(result)
            else:
                st.warning("Please enter a question.")
    
    with col2:
        st.header("ℹ️ How to Use")
        st.markdown("""
        **1. Upload Documents**
        - Click 'Browse files' in the sidebar
        - Select PDF, TXT, or DOCX files
        - Click 'Add to Knowledge Base'
        
        **2. Ask Questions**
        - Type your question in the text area
        - Click 'Search Knowledge Base'
        - Get AI-powered answers from your docs
        
        **3. Tips**
        - Be specific with your questions
        - You can upload multiple documents
        - The AI will find relevant information across all docs
        """)
        
        st.markdown("---")
        st.info("💡 **Tip:** Upload more documents to build a richer knowledge base!")


if __name__ == "__main__":
    main()
