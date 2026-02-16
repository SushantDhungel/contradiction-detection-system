from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import Annotated
import tempfile
import os

from schemas import (
    VerificationResponse,
    ErrorResponse,
    HealthResponse,
    SupportedTypesResponse,
    Verdict,
    TextChunkResponse,
)

from configs import Config
from database import SessionDep
from storage import MinioDep

# TODO:Add the Parser and Verfier
# from data_layer.parser import DocumentParser
# from nlp_layer.verifier import ClaimVerifier


router = APIRouter(prefix="/api/v1", tags=["api"])

config = Config()

# TODO: Initialize components DocumentParser and Claim Verifier


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
    description="""Upload a source document and verify a claim against it.
             **Process:**
             1. Parse the uploaded document
             2. Extract and chunk text
             3. Find relevant context using semantic search
             4. Verify claim using AI
             5. Return verdict with evidence
             """,
)
async def verify_claim(
    file: Annotated[UploadFile, File(description="Source document (PDF or TXT)")],
    claim: Annotated[str, Form(description="The claim to verify")],
    session: SessionDep,
    minio: MinioDep,
):
    """Main endpoint for claim verification.

    **Parameters:**
    - file: PDF or TXT document
    - claim: Statement to verify

    **Returns:**
    - Verdict (TRUE, FALSE, PARTIALLY_TRUE, CANNOT_DETERMINE)
    - Explanation
    - Evidence quotes from document
    - Confidence score
    - Relevant text chunks
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
                status_code=status.HTTP_413_CONTENT_TOO_LARGE,
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
            # TODO: Call Data Layer to parse document
            # chunks = document_parser.parse_and_chunk(temp_file.name)

            # MOCK DATA (remove when teammates finish their work)
            print(f"📄 Processing file: {file.filename}")  # ✅ Fixed
            print(f"📏 File size: {len(file_content)} bytes")
            print(f"🔍 Verifying claim: {claim}")

            # Mock response for testing
            response = VerificationResponse(
                verdict=Verdict.PARTIALLY_TRUE,
                explanation="[MOCK] This is a placeholder response. Waiting for Data Layer and NLP Layer implementation.",
                evidence=[
                    "[MOCK] Evidence will come from the document",
                    "[MOCK] AI will analyze and provide quotes",
                ],
                confidence=0.75,
                relevant_chunks=[
                    TextChunkResponse(
                        content="[MOCK] Relevant chunk from document will appear here",
                        chunk_index=0,
                        page_number=1,
                    )
                ],
            )

            # TODO: When the claim verifier is done
            # result = claim_verifier.verify(claim, chunks)
            # response = VerificationResponse(
            #     verdict=result.verdict,
            #     explanation=result.explanation,
            #     evidence=result.evidence,
            #     confidence=result.confidence,
            #     relevant_chunks=[
            #         TextChunkResponse(**chunk.model_dump())
            #         for chunk in result.relevant_chunks
            #     ]
            # )

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
    "/supported-types",
    response_model=SupportedTypesResponse,
    summary="Get supported file types",
    description="List of file extensions supported by the system",
)
async def get_supported_types():
    """
    Get list of supported document types.
    """
    return SupportedTypesResponse(
        supported=["*.pdf", ".txt"], coming_soon=[".docx", ".png", ".jpg", ".jpeg"]
    )
