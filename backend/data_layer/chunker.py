from dataclasses import dataclass
from typing import List

# ALGORITHM USED: Fixed-size sliding window algorithm with overlap
# Take a fixed number of characters (chunk_size)
# Move forward by a step smaller than chunk_size
# Repeat until the text ends


@dataclass
class TextChunk:
    # Represents a chunk of text with an ID
    content: str
    chunk_index: int  # Changed from chunk_id to match NLP layer
    metadata: dict = None  # Added metadata field for page numbers, etc.

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class TextChunker:
    # Splits text into fixed-size chunks with optional overlap.

    def __init__(self, chunk_size: int = 500, overlap: int = 100):

        # chunk_size (int): Number of characters per chunk.
        # overlap (int): Number of overlapping characters between consecutive chunks.

        if overlap >= chunk_size:
            raise ValueError("Overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[TextChunk]:

        # Split text into chunks.
        # Args: text (str): The full text to chunk.
        # Returns: List[TextChunk]: A list of chunk objects.

        chunks: List[TextChunk] = []
        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            chunks.append(TextChunk(content=chunk_text, chunk_index=chunk_index))

            # Move start forward with overlap
            start += self.chunk_size - self.overlap
            chunk_index += 1

        return chunks
