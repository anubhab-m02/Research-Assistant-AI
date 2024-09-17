from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
import re

def perform_semantic_search(query: str, corpus: List[str], top_k: int = 5) -> List[Dict[str, Any]]:
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    
    # Fit and transform the corpus
    corpus_vectors = vectorizer.fit_transform(corpus)
    
    # Transform the query
    query_vector = vectorizer.transform([query])
    
    # Calculate cosine similarities
    similarities = cosine_similarity(query_vector, corpus_vectors)[0]
    
    # Get top k results
    top_k_indices = similarities.argsort()[-top_k:][::-1]
    top_k_scores = similarities[top_k_indices]
    
    return [{"corpus_id": idx, "score": score} for idx, score in zip(top_k_indices, top_k_scores)]

def highlight_text(text: str, query: str) -> str:
    words = query.lower().split()
    pattern = r'\b(' + '|'.join(re.escape(word) for word in words) + r')\b'
    highlighted = re.sub(pattern, r'<mark>\1</mark>', text, flags=re.IGNORECASE)
    return highlighted
