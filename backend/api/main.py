from pathlib import Path
from turtle import title
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .routes import router

from dotenv import load_dotenv
import os

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("=" * 60)
    print("🚀 Contradiction Detection System API")
    print("=" * 60)

    # Initialze database
    try:
        from .database import init_db

        init_db()
        print("Database Initialized ✅")
    except Exception as e:
        print(f"⚠️ Database warning: {e}")

    # Initialize storage
    try:
        from .storage import init_storage

        init_storage()
        print("✅ Storage initialized")
    except Exception as e:
        print(f"⚠️ Storage Warning: {e}")

    print("=" * 60)
    print("API Docs: http://localhost:8000/v1/docs")
    print("Health Check: http://localhost:8000/api/v1/health")
    yield

    print("Shutting down API...")


title = "Contradiction Detection System API"
description = """
    AI-powered claim verification system.
    
    ## Features
    - Upload PDF/TXT documents
    - Verify claims against source documents
    - Get AI-powered verdicts with evidence
    - High accuracy using semantic search
    
    ## Team Integration
    This API integrates:
    - **Data Layer**: Document parsing and chunking
    - **NLP Layer**: Embeddings, search, and AI verification
    - **API Layer**: RESTful endpoints and validation
    """

origins = os.getenv("ORIGINS", "http://localhost:5173")

app = FastAPI(
    title=title,
    description=description,
    version="0.0.1",
    lifespan=lifespan,
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
def main():
    return {"message": "🚀🚀🚀API is running🚀🚀🚀"}
