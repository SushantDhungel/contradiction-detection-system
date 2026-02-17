import sys
import os

# Add backend folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from datalayer import DocumentParser

parser = DocumentParser(chunk_size=100, overlap=20)

# Build correct file path
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "certificate.pdf")

chunks = parser.parse(file_path)

print(f"Total chunks: {len(chunks)}")
for chunk in chunks:
    print(f"Chunk {chunk.chunk_id} ({len(chunk.content)} chars): {chunk.content[:100]}...")
