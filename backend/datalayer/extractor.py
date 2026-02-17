import pdfplumber
import unicodedata
import re

class TextExtractor:
    def extract(self, file_path: str) -> str:
        filename = file_path.lower()
        text_parts = []

        if filename.endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)

        elif filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text_parts.append(f.read())

        else:
            raise ValueError("Unsupported file type for parsing")

        full_text = "\n".join(text_parts)

        # Normalize encoding
        full_text = unicodedata.normalize("NFKC", full_text)

        # Clean whitespace
        full_text = re.sub(r"\s+", " ", full_text).strip()

        return full_text
