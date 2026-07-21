import numpy as np
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticVectorStore:
    """
    Vector storage and semantic retrieval engine powered by TF-IDF and Cosine Similarity vector space math.
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.chunks: List[Dict[str, Any]] = []
        self.matrix: Any = None

    def add_chunks(self, new_chunks: List[Dict[str, Any]]):
        """
        Indexes a list of document chunk dictionaries into vector space.
        """
        if not new_chunks:
            return

        self.chunks.extend(new_chunks)
        texts = [c["text"] for c in self.chunks]
        self.matrix = self.vectorizer.fit_transform(texts)

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Performs semantic vector similarity search against indexed document chunks.

        Returns:
            List of matching chunk dicts with similarity scores.
        """
        if not self.chunks or self.matrix is None:
            return []

        query_vec = self.vectorizer.transform([query])
        sim_scores = cosine_similarity(query_vec, self.matrix).flatten()

        # Get top-k indices sorted by similarity score
        top_indices = np.argsort(sim_scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            score = float(sim_scores[idx])
            if score > 0.0:  # Only return relevant non-zero matches
                chunk_data = dict(self.chunks[idx])
                chunk_data["similarity_score"] = round(score, 4)
                results.append(chunk_data)

        return results

    def clear(self):
        """Clears all indexed vectors and chunks."""
        self.chunks = []
        self.matrix = None

    def get_stats(self) -> Dict[str, Any]:
        """Returns statistics about indexed knowledge base."""
        files = {c["file_path"] for c in self.chunks}
        return {
            "total_chunks": len(self.chunks),
            "unique_files_count": len(files),
            "files": list(files),
            "vocabulary_size": len(self.vectorizer.vocabulary_) if hasattr(self.vectorizer, "vocabulary_") else 0,
        }
