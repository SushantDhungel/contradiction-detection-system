"""
Contradiction Detection System API

Main FastAPI application entry point.
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

from .routes import router  # ✅ Fixed: relative import

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    print("=" * 60)
    print("🚀 Contradiction Detection System API")
    print("=" * 60)

    # Initialize database
    try:
        from .database import init_db

        init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️  Database warning: {e}")

    # Initialize storage
    try:
        from .storage import init_storage

        print("✅ Storage initialized")
    except Exception as e:
        print(f"⚠️  Storage warning: {e}")

    print("=" * 60)
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/api/health")
    print("=" * 60)

    yield

    # Shutdown
    print("👋 Shutting down API...")


# Create FastAPI app
app = FastAPI(
    title="Contradiction Detection System API",
    description="""
    **Contradiction Detection System** - AI-powered claim verification against source documents.
    
    ## Features
    
    * **Upload Documents**: PDF or TXT files
    * **Verify Claims**: Check if statements are true, false, or partially true
    * **Get Evidence**: Receive relevant quotes and explanations
    * **High Accuracy**: Powered by semantic search and AI
    
    ## How It Works
    
    1. Upload a source document (PDF/TXT)
    2. Provide a claim to verify
    3. System extracts text and finds relevant context
    4. AI analyzes and returns verdict with evidence
    
    ## Team Integration
    
    This API integrates three layers:
    - **Data Layer**: Document parsing and chunking
    - **NLP Layer**: Embeddings, search, and AI verification
    - **API Layer**: RESTful endpoints and validation
    
    ## Example
    
    **Document**: Sales Report Q3 2025
    
    **Claim**: "Revenue increased by 25%"
    
    **Result**: PARTIALLY_TRUE - Revenue increased by 20%, not 25%
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",  # ✅ Fixed: standard path
    redoc_url="/redoc",
)

# Get allowed origins from environment
origins = os.getenv(
    "ORIGINS",
    "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173",
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins.split(","),  # ✅ Support multiple origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)  # ✅ Added: include the router


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint - API welcome message.
    """
    return {
        "message": "🎯 Contradiction Detection System API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/health",
    }


@app.get("/ping", tags=["root"])
async def ping():
    """
    Simple ping endpoint for quick testing.
    """
    return {"ping": "pong"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
