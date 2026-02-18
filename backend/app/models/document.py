"""
Document Database Model

Stores metadata about uploaded documents in PostgreSQL.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional


class DocumentType(str, Enum):
    """Supported document types."""

    PDF = "pdf"
    TXT = "txt"
    # Future support (when Data Layer implements):
    # CSV = "csv"
    # DOCX = "docx"
    # PNG = "png"
    # JPG = "jpg"


class Document(SQLModel, table=True):
    """
    Document metadata stored in PostgreSQL.

    This model is ready for future use if you decide to add:
    - Document storage/history
    - Verification audit trail
    - Re-verification of previously uploaded docs

    Currently, the API processes documents ephemerally (no storage).
    """

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # File information
    file_name: str = Field(..., max_length=255, description="Original filename")
    file_path: str = Field(..., max_length=512, description="Path in MinIO storage")
    file_size: int = Field(..., gt=0, description="File size in bytes")
    doc_type: DocumentType = Field(..., description="Document type")

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Upload timestamp"
    )

    # Optional fields (for future enhancement)
    # Uncomment when needed:
    # content_hash: Optional[str] = Field(default=None, max_length=64)
    # uploaded_by: Optional[str] = Field(default=None, max_length=100)
    # verification_count: int = Field(default=0, description="Times verified")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "file_name": "sales_report_q3.pdf",
                "file_path": "documents/2026/02/sales_report_q3.pdf",
                "file_size": 2548736,
                "doc_type": "pdf",
                "created_at": "2026-02-16T10:30:00",
            }
        }
