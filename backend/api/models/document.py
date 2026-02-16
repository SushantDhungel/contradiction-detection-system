from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    PDF = "pdf"
    TXT = "txt"
    CSV = "csv"
    XLS = "xls"
    JPEG = "jpeg"


class Document(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    file_name: str
    file_path: str
    file_size: int
    doc_type: DocumentType


# TODO: Might need discuss
# about vectorization of the document -> Generating Embeddings
