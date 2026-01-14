"""
Advanced features module for Second Brain AI
This file contains enhanced functionality that can be gradually added to the main app.
"""

import json
from typing import List, Dict
from datetime import datetime


class ConversationHistory:
    """Manages conversation history for context-aware queries."""
    
    def __init__(self, max_history: int = 10):
        self.history = []
        self.max_history = max_history
    
    def add_interaction(self, query: str, response: str, sources: List[str]):
        """Add a query-response pair to history."""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "sources": sources
        }
        self.history.append(interaction)
        
        # Keep only the most recent interactions
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_context(self, last_n: int = 3) -> str:
        """Get recent conversation context."""
        recent = self.history[-last_n:] if len(self.history) >= last_n else self.history
        context = ""
        for interaction in recent:
            context += f"Previous Q: {interaction['query']}\n"
            context += f"Previous A: {interaction['response']}\n\n"
        return context
    
    def save_to_file(self, filepath: str):
        """Save conversation history to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def load_from_file(self, filepath: str):
        """Load conversation history from JSON file."""
        try:
            with open(filepath, 'r') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []


class DocumentAnalyzer:
    """Provides advanced document analysis capabilities."""
    
    @staticmethod
    def extract_key_topics(documents: List[str], top_n: int = 5) -> List[str]:
        """Extract key topics from documents using TF-IDF."""
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        vectorizer = TfidfVectorizer(max_features=top_n, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        feature_names = vectorizer.get_feature_names_out()
        return list(feature_names)
    
    @staticmethod
    def summarize_document(text: str, max_sentences: int = 3) -> str:
        """Generate a brief summary of a document."""
        sentences = text.split('.')
        # Simple extractive summarization - take first few sentences
        summary_sentences = sentences[:max_sentences]
        return '. '.join(summary_sentences) + '.'
    
    @staticmethod
    def calculate_readability_score(text: str) -> Dict[str, float]:
        """Calculate readability metrics for a document."""
        import textstat
        
        return {
            "flesch_reading_ease": textstat.flesch_reading_ease(text),
            "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
            "gunning_fog": textstat.gunning_fog(text)
        }


class SmartRetriever:
    """Enhanced retrieval with query expansion and filtering."""
    
    @staticmethod
    def expand_query(query: str, expansion_terms: int = 3) -> str:
        """Expand query with related terms for better retrieval."""
        # This is a placeholder - in production, use word embeddings
        # or a language model for semantic expansion
        expanded = query
        # Add synonyms or related terms
        return expanded
    
    @staticmethod
    def rerank_results(query: str, documents: List[Dict], top_k: int = 4) -> List[Dict]:
        """Rerank retrieved documents based on relevance."""
        # Implement cross-encoder reranking for better results
        # For now, return top_k documents
        return documents[:top_k]
    
    @staticmethod
    def filter_by_metadata(documents: List[Dict], filters: Dict) -> List[Dict]:
        """Filter documents based on metadata criteria."""
        filtered = documents
        
        if 'date_range' in filters:
            start, end = filters['date_range']
            filtered = [d for d in filtered 
                       if start <= d.get('date', datetime.max) <= end]
        
        if 'source_type' in filters:
            filtered = [d for d in filtered 
                       if d.get('source_type') == filters['source_type']]
        
        return filtered


class ExportManager:
    """Handles exporting data in various formats."""
    
    @staticmethod
    def export_to_markdown(conversations: List[Dict], filepath: str):
        """Export conversation history to markdown."""
        with open(filepath, 'w') as f:
            f.write("# Second Brain AI - Conversation Export\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            for i, conv in enumerate(conversations, 1):
                f.write(f"## Query {i}\n\n")
                f.write(f"**Question:** {conv['query']}\n\n")
                f.write(f"**Answer:** {conv['response']}\n\n")
                if conv.get('sources'):
                    f.write("**Sources:**\n")
                    for source in conv['sources']:
                        f.write(f"- {source}\n")
                f.write("\n---\n\n")
    
    @staticmethod
    def export_to_json(data: Dict, filepath: str):
        """Export data to JSON format."""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def create_knowledge_graph(documents: List[Dict]) -> Dict:
        """Create a simple knowledge graph from documents."""
        # Placeholder for knowledge graph creation
        # In production, use spaCy or similar for entity extraction
        graph = {
            "nodes": [],
            "edges": []
        }
        return graph


class PerformanceMonitor:
    """Monitor and log system performance metrics."""
    
    def __init__(self):
        self.metrics = {
            "query_count": 0,
            "avg_response_time": 0,
            "total_documents": 0,
            "cache_hits": 0
        }
    
    def log_query(self, response_time: float):
        """Log a query execution."""
        self.metrics["query_count"] += 1
        
        # Update average response time
        prev_avg = self.metrics["avg_response_time"]
        count = self.metrics["query_count"]
        self.metrics["avg_response_time"] = (
            (prev_avg * (count - 1) + response_time) / count
        )
    
    def get_stats(self) -> Dict:
        """Get current performance statistics."""
        return self.metrics.copy()


# Example usage functions that can be integrated into main app

def add_conversation_memory(query_function):
    """Decorator to add conversation memory to query function."""
    history = ConversationHistory()
    
    def wrapper(query, *args, **kwargs):
        # Add previous context to query
        context = history.get_context()
        enhanced_query = f"{context}\nCurrent question: {query}"
        
        # Execute query
        result = query_function(enhanced_query, *args, **kwargs)
        
        # Save to history
        history.add_interaction(query, result.get('result', ''), 
                               result.get('sources', []))
        
        return result
    
    return wrapper


def batch_process_documents(file_paths: List[str], brain_instance):
    """Process multiple documents at once."""
    results = []
    for file_path in file_paths:
        success, message = brain_instance.add_to_knowledge_base(file_path)
        results.append({
            "file": file_path,
            "success": success,
            "message": message
        })
    return results


def suggest_related_queries(current_query: str, document_topics: List[str]) -> List[str]:
    """Suggest related queries based on document topics."""
    # Simple implementation - in production, use semantic similarity
    suggestions = [
        f"Tell me more about {topic}" for topic in document_topics[:3]
    ]
    suggestions.append(f"How does {current_query} relate to {document_topics[0]}?")
    return suggestions


if __name__ == "__main__":
    # Example usage
    print("Advanced features module loaded successfully!")
    print("\nAvailable enhancements:")
    print("- Conversation History")
    print("- Document Analysis")
    print("- Smart Retrieval")
    print("- Export Management")
    print("- Performance Monitoring")
