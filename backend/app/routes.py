"""
API Routes

FastAPI endpoints for the Contradiction Detection System.
Integrates with Data Layer and NLP Layer built by teammates.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import Annotated
import tempfile
import os

from app.schemas import (
    VerificationResponse,
    ErrorResponse,
    HealthResponse,
    SupportedTypesResponse,
    Verdict,
    TextChunkResponse,
)
from app.configs import Config
from app.database import SessionDep
from app.storage import MinioDep

from data_layer import DocumentParser
from nlp_layer import ClaimVerifier

router = APIRouter(prefix="/api", tags=["verification"])

config = Config()


# Initialize parser and verifier (singleton instances)
parser = DocumentParser()
verifier = ClaimVerifier()


@router.post(
    "/verify",
    response_model=VerificationResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        413: {"model": ErrorResponse, "description": "File too large"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
    summary="Verify a claim against a document",
    description="""
Upload a source document and verify a claim against it.

### Process
1. **Parse** the uploaded document (PDF/TXT)
2. **Extract and chunk** text
3. **Find relevant context** using semantic search
4. **Verify claim** using AI
5. **Return verdict** with evidence
""",
)
async def verify_claim(
    file: Annotated[UploadFile, File(description="Source document (PDF or TXT)")],
    claim: Annotated[str, Form(description="The claim to verify")],
    session: SessionDep,
    minio: MinioDep,
):
    """
    Main endpoint for claim verification.

    ### Parameters
    - **file**: PDF or TXT document
    - **claim**: Statement to verify

    ### Returns
    - **verdict**: TRUE, FALSE, PARTIALLY_TRUE, or CANNOT_DETERMINE
    - **explanation**: Explanation of the verdict
    - **evidence**: Evidence quotes from document
    - **confidence**: Confidence score (0-1)
    - **relevant_chunks**: Relevant text chunks
    """

    # 1. Validate claim
    if not claim or len(claim.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(
                error="Invalid claim", detail="Claim cannot be empty"
            ).model_dump(),
        )

    # 2. Validate file type
    filename = file.filename.lower()
    if not (filename.endswith(".pdf") or filename.endswith(".txt")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(
                error="Unsupported file type",
                detail=f"File '{file.filename}' is not supported. Use PDF or TXT files.",
            ).model_dump(),
        )

    try:
        # 3. Read file content
        file_content = await file.read()

        # 4. Validate file size (10MB max)
        MAX_FILE_SIZE = 10 * 1024 * 1024
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=ErrorResponse(
                    error="File too large", detail="File size must be less than 10MB"
                ).model_dump(),
            )

        # 5. Check if file is empty
        if len(file_content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorResponse(
                    error="Empty file", detail="Uploaded file is empty"
                ).model_dump(),
            )

        # 6. Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(file.filename)[1]
        )
        temp_file.write(file_content)
        temp_file.close()

        try:
            # Parse document and chunk
            chunks = parser.parse(temp_file.name)
            if not chunks:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorResponse(
                        error="No text extracted",
                        detail="The uploaded file could not be parsed or is empty.",
                    ).model_dump(),
                )

            # Verify claim using the NLP layer
            result = verifier.verify(chunks, claim)

            # Build API response
            response = VerificationResponse(
                verdict=Verdict(result.verdict),
                explanation=result.explanation,
                evidence=result.evidence,
                confidence=result.confidence,
                relevant_chunks=[
                    TextChunkResponse(
                        content=chunk.content,
                        chunk_index=chunk.chunk_index,
                        page_number=(
                            chunk.metadata.get("page") if chunk.metadata else None
                        ),
                    )
                    for chunk in result.relevant_chunks
                ],
            )
            return response

        finally:
            # Cleanup temp file
            try:
                os.unlink(temp_file.name)
            except Exception as cleanup_error:
                print(f"⚠️ Failed to cleanup temp file: {cleanup_error}")

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in verify_claim: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="Internal server error", detail=str(e)
            ).model_dump(),
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="""
Check if API and all services are running correctly.

Verifies:
- Database connection
- Storage (MinIO) connection
- Configuration loaded
""",
)
async def health_check():
    """
    Health check endpoint.

    Verifies that all services are available:
    - **Database connection**
    - **Storage (MinIO) connection**
    - **Configuration loaded**
    """
    services = {}

    # Check database
    try:
        from .database import engine

        with engine.connect() as conn:
            services["database"] = "connected"
    except Exception as e:
        services["database"] = f"error: {str(e)}"

    # Check storage
    try:
        from .storage import minio_client

        bucket_name = config.MINIO_BUCKET_NAME
        if minio_client.bucket_exists(bucket_name):
            services["storage"] = "connected"
        else:
            services["storage"] = "bucket_not_found"
    except Exception as e:
        services["storage"] = f"error: {str(e)}"

    # Check configuration
    try:
        if config.MINIO_ROOT_USER:
            services["config"] = "loaded"
        else:
            services["config"] = "incomplete"
    except Exception as e:
        services["config"] = f"error: {str(e)}"

    # Determine overall status
    all_healthy = all(
        "connected" in str(v) or "loaded" in str(v) for v in services.values()
    )

    return HealthResponse(
        status="healthy" if all_healthy else "degraded",
        version="1.0.0",
        services=services,
    )


@router.get(
    "/supported-types",
    response_model=SupportedTypesResponse,
    summary="Get supported file types",
    description="""
List of file extensions supported by the system.

**Currently supported:** .pdf, .txt
**Coming soon:** .docx, .png, .jpg, .jpeg
""",
)
async def get_supported_types():
    """
    Get list of supported document types.

    Returns current and planned file type support.
    """
    return SupportedTypesResponse(
        supported=[".pdf", ".txt"],  # ✅ Fixed: removed asterisk
        coming_soon=[".docx", ".png", ".jpg", ".jpeg"],
    )
