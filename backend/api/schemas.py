from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class Verdict(str, Enum):
    """Possible verdicts for claim verification"""

    TRUE = "TRUE"
    FALSE = "FALSE"
    PARTIALLY_TRUE = "PARTIALLY TRUE"
    CANNOT_DETERMINE = "CANNON_DETERMINE"


class TextChunkResponse(BaseModel):
    """A chunk of text from the source document."""

    content: str
    chunk_index: int
    page_number: Optional[int] = None


class VerificationRequest(BaseModel):
    """
    Request body for claim verfication
    File is uploaded separately via multipart/form-data.
    """

    claim: str = Field(..., min_length=1, description="The claim to verify")

    class Config:
        json_schema_extra = {"example": {"claim": "Revenue increased by 25% in Q3"}}


class VerificationResponse(BaseModel):
    """Response after claim verification."""

    verdict: Verdict
    explanation: str
    evidence: List[str]
    confidence: float = Field(..., ge=0.0, le=1.0)
    relevant_chunks: List[TextChunkResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "verdict": "PARTIALLY TRUE",
                "explanation": "Revenue increased by 20%, not 25%",
                "evidence": ["Q3 2025 revenue was $4.5M", "Q3 2024 revenue was $3.5M"],
                "confidence": 0.85,
                "relevant_chunks": [
                    {
                        "content": "Q3 reveneue was $4.2 million...",
                        "chunk_index": 0,
                        "page_number": 1,
                    }
                ],
            }
        }


class ErrorResponse(BaseModel):
    """Standard Error Response"""

    error: str
    detail: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Unsupported file type",
                "detail": "Only PDF and TXT files are supported",
            }
        }


class HealthResponse(BaseModel):
    """Health Check Response"""

    status: str
    version: str
    services: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "services": {
                    "database": "connected",
                    "storage": "connected",
                },
            }
        }


class SupportedTypesResponse(BaseModel):
    """Supported file types response."""

    supported: List[str]
    coming_soon: Optional[List[str]] = None
