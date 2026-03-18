import numpy as np
from sentence_transformers import SentenceTransformer


class EndeeVectorStore:
    """
    Endee-inspired vector database abstraction for storing and searching
    text embeddings using cosine similarity.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.chunks: list[str] = []
        self.embeddings: np.ndarray | None = None

    def add_chunks(self, chunks: list[str]) -> None:
        """Embed and store text chunks."""
        self.chunks = chunks
        self.embeddings = self.model.encode(chunks, normalize_embeddings=True)

    def search(self, query: str, top_k: int = 5) -> list[str]:
        """Return the top_k most similar chunks to the query."""
        if not self.chunks or self.embeddings is None:
            return []
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        scores = np.dot(self.embeddings, query_embedding.T).flatten()
        top_k = min(top_k, len(self.chunks))
        top_indices = np.argsort(scores)[::-1][:top_k]
        # Only return chunks with a reasonable similarity
        return [self.chunks[i] for i in top_indices if scores[i] > 0.05]

    def get_all_chunks(self) -> list[str]:
        """Return all stored chunks (useful for full-context answers)."""
        return list(self.chunks)

    def clear(self) -> None:
        """Reset the store."""
        self.chunks = []
        self.embeddings = None


