"""
Database Models

SQLModel models for PostgreSQL database tables.
Separate from API schemas (Pydantic) in schemas.py.
"""

from .document import Document, DocumentType

__all__ = ["Document", "DocumentType"]
