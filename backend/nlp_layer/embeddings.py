"""
Using pre-trained model called all-MiniLM-L6-v2 for 384-dimensional embeddings.

Text Embedding Module
This module converts text into numerical vectors (embeddings)
that capture the meaning of the text.

"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List


class EmbeddingGenerator:
    """
    Converts text into numerical embeddings.

    Uses Sentence Transformers, which are pre-trained models
    that understand the meaning of text

    Example:
    embedder = EmbeddingGenerator()
    vector = embedder.embed_single("Hello World")
    print(vector.shape) #(384,) - a list of 384 numbers
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize with a sentence transformer model.

        Args:
            model_name: The HuggingFace model to use.
                Default is "all-MiniLM-L6-v2" which is:
                -Fast (small model)
                -Good quality embeddings
                -384 - dimensional output

        """
        print(f"Loading embedding model: {model_name}...")
        print("This may take a minute the first time")

        # Load the model (downloads automatically if not cached)
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

        print(f" Model loaded! Embedding dimensions: {self.embedding_dim}")

    def embed_single(self, text: str) -> np.ndarray:

        # encode() returns a 2D array, we take [0] to get 1D

        embedding = self.model.encode([text], convert_to_numpy=True)[0]
        return embedding

    def embed_batch(self, texts: List[str]) -> np.ndarray:

        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings

    def cosine_similarity(self, vec_a: np.ndarray, vec_b: np.ndarray) -> float:

        # Normalize vectors (make them length 1)
        norm_a = vec_a / np.linalg.norm(vec_a)
        norm_b = vec_b / np.linalg.norm(vec_b)

        # Dot product of normalized vectors = cosine similarity
        return float(np.dot(norm_a, norm_b))


if __name__ == "__main__":
    print("=" * 50)
    print("Testing Embedding Generator")
    print("=" * 40)

    # Create embedder
    embedder = EmbeddingGenerator()

    # Test 1: Embed a single text

    print("\n test 1: single embedding--")
    text = "The company revenue increased by 20%"
    embedding = embedder.embed_single(text)
    print(f"Text: '{text}'")
    print(f"Embedding shape: {embedding.shape}")
    print(f"First 5 values: {embedding[:5]}")

    # Test 2: Compare similar texts
    print("\n -- Test 2: Similarity Comarison ---")
    texts = [
        "Revenue grew by 25%",
        "Sales increased Significantly",
        "The weather is sunny today",
    ]
    query = "Company earnings went up"

    query_embedding = embedder.embed_single(query)
    text_embeddings = embedder.embed_batch(texts)

    print(f"Query: '{query}'")
    print("\n Similarities:")
    for i, text in enumerate(texts):
        sim = embedder.cosine_similarity(query_embedding, text_embeddings[i])
        print(f" {sim:.3f} = '{text}'")

    # Test 3: Batch embedding
    print("\n --- Test 3: Batch Embedding ---")
    batch = ["Hello", "World", "Python"]
    batch_embeddings = embedder.embed_batch(batch)
    print(f"Batch of {len(batch)} texts -> Shape: {batch_embeddings.shape}")

    print("\n" + "=" * 50)
    print("All test passed!")
