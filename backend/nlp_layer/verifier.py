"""
Claim Verifier

This is the main module that brings everything together:
1. Takes document chunks and a claim
2. Finds relevant context using semantic search
3. Asks Gemini to verify the claim
4. Returns a structured result
"""

from typing import List, Optional
from dataclasses import dataclass
from enum import Enum
import json
import re

from .embeddings import EmbeddingGenerator
from .search import SemanticSearch
from data_layer.chunker import TextChunk
from .gemini_client import GeminiClient


class Verdict(str, Enum):
    """Possible verification outcomes."""

    TRUE = "TRUE"
    FALSE = "FALSE"
    PARTIALLY_TRUE = "PARTIALLY_TRUE"
    CANNOT_DETERMINE = "CANNOT_DETERMINE"


@dataclass
class VerificationResult:
    """
    The result of verifying a claim.

    Attributes:
        verdict: The determination (True/false)
        explanation: Why this verdict was reached
        evidence: Relevant quotes from the source
        confidence: How confident the system is (0-1)
        relevant_chunks: The chunks used for verification
    """

    verdict: Verdict
    explanation: str
    evidence: List[str]
    confidence: float
    relevant_chunks: List[TextChunk]

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "verdict": self.verdict.value,
            "explanation": self.explanation,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "relevant_chunks": [
                {"content": c.content, "index": c.chunk_index}
                for c in self.relevant_chunks
            ],
        }


class ClaimVerifier:
    """
    Verifies claims against source documents.

    This class orchestrates the entire verification process:
    1. Semantic search to find relevant context
    2. Prompt construction
    3. LLM call for verification
    4. Response parsing
    """

    # The prompt template for verification
    PROMPT_TEMPLATE = """ You are a fact-checking expert. Your job is to verify whether a claim is supported by the provided source text.
    
    --- Source Text ---
    {context}
    
    --- Claim to verifiy ---
    {claim}
    
    --- Your task ---
    Analyze the claim against the source text and determine if it's accurate.
    
    Respond with Only a JSON object in this exact format:
    {{
        "verdict": "TRUE" or "FALSE" or "PARTIALLY_TRUE" or "CANNOT_DETERMINE",
        "explanation": "A clear explanation of why you reached this verdict",
        "evidence":["relevant quote 1 from source", "relevant quote 2 if applicable"],
        "confidence": <number between 0.0 and 1.0>
    }}
    
    --- Important rules ---
    1. Only use information from the provided source text.
    2. If the source doesn't contain enough information, use "CANNOT_DETERMINE"
    3. For "PARTIALLY_TRUE", explain which parts are true and which are false
    4. Always cite specific evidence from the source
    5. Be precise with numbers - verify calculations if needed
    
    Respond with only the JSON object, no other text.
    """

    def __init__(self):
        """Initialize the verifier with all required components."""
        print("Initializing Claim Verifier...")

        # Create the embedding generator
        self.embedder = EmbeddingGenerator()

        # Create the semantic search engine
        self.search = SemanticSearch(self.embedder)

        # Create the Gemini client
        self.gemini = GeminiClient()

        print("Claim Verifier Ready!")

    def verify(
        self, chunks: List[TextChunk], claim: str, top_k: int = 5
    ) -> VerificationResult:
        """
        Verify a claim against document chunks.

        Args:
            Chunks: List of text chunks from the source document
            claim: The claim/statement to verify
            top_k: Number of relevant chunks to use for context

        Returns:
            VerificationResult with verdict and explanation
        """

        print(f"Verifying claim: '{claim}'")
        print("-" * 50)

        # Step 1: Index the chunks for searching
        print("Step 1: Indexing document chunks...")
        self.search.index_chunks(chunks)

        # Step 2: Find relevant chunks
        print(f"Step 2: Finding top {top_k} relevant chunks...")
        search_results = self.search.search(claim, top_k=top_k)
        relevant_chunks = [chunk for chunk, score in search_results]

        # Log what we found
        print("Found relevant context:")
        for chunk, score in search_results:
            preview = chunk.content[:60].replace("\n", " ")
            print(f"  [{score:.3f}] {preview}...")

        # Step 3: Build context from relevant chunks
        print("Step 3: Building context for LLM...")
        context = self._build_context(search_results)

        # Step 4: Build the prompt
        print("Step 4: Constructing prompt...")
        prompt = self.PROMPT_TEMPLATE.format(context=context, claim=claim)

        # Step 5: Call Gemini
        print("Step 5: Calling Gemini API...")
        response = self.gemini.generate(prompt)

        # Step 6: Parse the response
        print("Step 6: Parsing response...")
        result = self._parse_response(response, relevant_chunks)

        print("-" * 50)
        print(f"Verdict: {result.verdict.value}")

        return result

    def _build_context(self, search_results: List[tuple]) -> str:
        """
        Build a context string from search results.

        Args:
            search_results: List of (chunk, score) tuples

        Returns:
            Formatted context string for the prompt
        """
        context_parts = []

        for chunk, score in search_results:
            # Include chunk number for reference
            context_parts.append(
                f"[Chunk {chunk.chunk_index}] (relevance: {score:.2f}):\n"
                f"{chunk.content}"
            )

        return "\n\n".join(context_parts)

    def _parse_response(
        self, response: str, relevant_chunks: List[TextChunk]
    ) -> VerificationResult:
        """
        Parse Gemini's response into a VerificationResult.

        Args:
            response: Raw response from Gemini
            relevant_chunks: The chunks used for context

        Returns:
            Parsed VerificationResult
        """
        try:
            # Try to extract JSON from the response
            # Sometimes LLMs add extra text around the JSON
            json_match = re.search(r"\{.*\}", response, re.DOTALL)

            if not json_match:
                raise ValueError("No JSON found in response")

            # Parse the JSON
            data = json.loads(json_match.group())

            # Extract and validate fields
            verdict_str = data.get("verdict", "CANNOT_DETERMINE").upper()
            verdict = Verdict(verdict_str)

            return VerificationResult(
                verdict=verdict,
                explanation=data.get("explanation", "No explanation provided"),
                evidence=data.get("evidence", []),
                confidence=float(data.get("confidence", 0.5)),
                relevant_chunks=relevant_chunks,
            )

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # If parsing fails, return a fallback result
            print(f"Warning: Could not parse response: {e}")
            print(f"Raw response: {response[:200]}...")

            return VerificationResult(
                verdict=Verdict.CANNOT_DETERMINE,
                explanation=f"Error parsing AI response: {str(e)}",
                evidence=[],
                confidence=0.0,
                relevant_chunks=relevant_chunks,
            )


# --- Test the complete system ---
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Complete Claim Verifier")
    print("=" * 60)

    # Create verifier
    verifier = ClaimVerifier()

    # Create sample document chunks (simulated sales report)
    chunks = [
        TextChunk(
            content="Q3 2025 Financial Results Summary:\n"
            "Total revenue for Q3 2025 reached $4.2 million. "
            "This represents an increase from Q2 2025 revenue of $3.8 million.",
            chunk_index=0,
        ),
        TextChunk(
            content="Growth Analysis:\n"
            "Quarter-over-quarter growth was 10.5%, calculated as "
            "(4.2 - 3.8) / 3.8 = 0.105 or 10.5%. "
            "Year-over-year growth compared to Q3 2024 was 23%.",
            chunk_index=1,
        ),
        TextChunk(
            content="Customer Metrics:\n"
            "New customer acquisitions: 45 accounts\n"
            "Customer churn rate: 2.1%\n"
            "Net Promoter Score: 72",
            chunk_index=2,
        ),
        TextChunk(
            content="Operational Updates:\n"
            "The company expanded its workforce to 150 employees, "
            "up from 120 in the previous quarter. "
            "New office opened in Austin, Texas.",
            chunk_index=3,
        ),
        TextChunk(
            content="Product Development:\n"
            "Version 3.0 of the main product was released in August. "
            "Three new features were added based on customer feedback.",
            chunk_index=4,
        ),
    ]

    # Test claims
    test_claims = [
        # This should be FALSE (10.5%, not 25%)
        "Q3 revenue grew by 25% compared to Q2",
        # This should be TRUE
        "The company has 150 employees",
        # This should be PARTIALLY_TRUE or CANNOT_DETERMINE
        "Revenue doubled in Q3",
        # This should be TRUE
        "Year-over-year growth was 23%",
    ]

    print("\n" + "=" * 60)
    print("Running Verification Tests")
    print("=" * 60)

    for claim in test_claims:
        print("\n" + "=" * 60)
        result = verifier.verify(chunks, claim)

        print(f"\n RESULT SUMMARY:")
        print(f"   Claim: {claim}")
        print(f"   Verdict: {result.verdict.value}")
        print(f"   Confidence: {result.confidence:.0%}")
        print(f"   Explanation: {result.explanation}")
        if result.evidence:
            print(f"   Evidence: {result.evidence}")

    print("\n" + "=" * 60)
    print("All tests completed!")
