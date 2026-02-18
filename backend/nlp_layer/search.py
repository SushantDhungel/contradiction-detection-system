"""
This code finds relevant text chunks based on meaning, not just keyword matching.

Key insight: We embed both the chunks and the query,then
find chunks whose embeddings are closest to the query.
"""

from typing import List, Tuple
import numpy as np

# Import TextChunk from data_layer to ensure consistency
from data_layer.chunker import TextChunk


class SemanticSearch:
    """
    Finds relevant text chunks using semantic similarity.

    How it works:
    1. Index: Convert all chunks to embeddings
    2. Search: Convert query to embedding, find closest chunks
    """

    def __init__(self, embedding_generator):
        self.embedder = embedding_generator
        self.chunks = None
        self.chunk_embeddings = None
        self._is_indexed = False

    def index_chunks(self, chunks: List[TextChunk]) -> None:
        """
        Index chunks for searching. Call this once per document.
        This pre-computes embeddings for all chunks so that
        searching is fast.
        """
        if not chunks:
            raise ValueError("No chunks provided!")
        print(f"Indexing {len(chunks)} chunks----")

        self.chunks = chunks

        texts = [chunk.content for chunk in chunks]
        self.chunk_embeddings = self.embedder.embed_batch(texts)

        self._is_indexed = True

        print(f"Indexed {len(chunks)} chunks")

    def search(self, query: str, top_k: int = 5) -> List[Tuple[TextChunk, float]]:
        """
        Find the most relevant chunks for a query.

        Args:
            query: The search query (e.g., user's claim)
            top_k: Number of results to return

        Returns:
            List of (chunk, similarity_score) tuples,
            sorted by relevance (highest first)
        """

        if not self._is_indexed:
            raise ValueError("No chunks indexed! Call index_chunks first.")

        query_embedding = self.embedder.embed_single(query)

        similarities = self._calculate_similarities(
            query_embedding, self.chunk_embeddings
        )

        top_indices = np.argsort(similarities)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            chunk = self.chunks[idx]
            score = float(similarities[idx])
            results.append((chunk, score))

        return results

    def _calculate_similarities(
        self, query_vec: np.ndarray, doc_vecs: np.ndarray
    ) -> np.ndarray:
        """
        Calculate cosine similarity between query and all documents.

        Args:
            query_vec: Query embedding (1D array)
            doc_vecs: Document embeddings (2D array)

        Returns:
            Array of similarity scores
        """

        # Normalize query
        query_norm = query_vec / np.linalg.norm(query_vec)

        # Normalize all document vectors
        doc_norms = np.linalg.norm(doc_vecs, axis=1, keepdims=True)
        doc_vecs_normalized = doc_vecs / doc_norms

        # Dot product with normalized vectors = cosine similarity
        similarities = np.dot(doc_vecs_normalized, query_norm)

        return similarities


# --- Test and demonstrate ---
if __name__ == "__main__":
    from embeddings import EmbeddingGenerator

    print("=" * 60)
    print("Testing Semantic Search")
    print("=" * 60)

    # Create embedder and search
    embedder = EmbeddingGenerator()
    search = SemanticSearch(embedder)

    # Create sample document chunks (simulating a sales report)
    chunks = [
        TextChunk(
            content="Q3 2025 Financial Summary: Total revenue reached $4.2 million, representing a 10.5% increase compared to Q2.",
            chunk_index=0,
            metadata={"page": 1},
        ),
        TextChunk(
            content="The company expanded its workforce to 150 employees, up from 120 in the previous quarter.",
            chunk_index=1,
            metadata={"page": 2},
        ),
        TextChunk(
            content="Customer acquisition cost (CAC) decreased by 15% due to improved marketing efficiency.",
            chunk_index=2,
            metadata={"page": 3},
        ),
        TextChunk(
            content="New product launches contributed $500,000 to Q3 revenue, exceeding projections by 20%.",
            chunk_index=3,
            metadata={"page": 4},
        ),
        TextChunk(
            content="The weather in Seattle was particularly rainy during Q3, affecting outdoor events.",
            chunk_index=4,
            metadata={"page": 5},
        ),
    ]

    # Index the chunks
    print("\n--- Indexing ---")
    search.index_chunks(chunks)

    # Test search queries
    test_queries = [
        "What was the Q3 revenue?",
        "How many employees does the company have?",
        "Tell me about new product performance",
    ]

    print("\n--- Search Results ---")
    for query in test_queries:
        print(f"\n Query: '{query}'")
        print("-" * 40)

        results = search.search(query, top_k=2)

        for i, (chunk, score) in enumerate(results, 1):
            print(f"  #{i} (score: {score:.3f}):")
            print(f"     {chunk.content[:80]}...")

    print("\n" + "=" * 60)
    print(" Semantic search is working!")
