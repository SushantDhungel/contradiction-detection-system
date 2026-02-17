import os
from typing import List
from .extractor import TextExtractor
from .chunker import TextChunk, TextChunker

class DocumentParser:
    # Orchestrates document parsing: extraction + cleaning + chunking

    def __init__(self, chunk_size: int = 500, overlap: int = 100):
        self.extractor = TextExtractor()
        self.chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)

    def parse(self, file_path: str) -> List[TextChunk]:

        # Parse a document into cleaned, chunked text.
        # Args:file_path (str): Path to PDF or TXT file.
        # Returns:List[TextChunk]: List of text chunks.

        self._validate_file(file_path)

        # Extract and clean text
        text = self.extractor.extract(file_path)

        # If text is empty, return empty list
        if not text:
            return []

        # Chunk text
        return self.chunker.chunk(text)

    def _validate_file(self, file_path: str):
        # Check if file exists and is a supported type
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} does not exist")

        if not file_path.lower().endswith((".pdf", ".txt")):
            raise ValueError("Only PDF and TXT files are supported")
