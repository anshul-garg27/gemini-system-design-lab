"""
Main FastAPI application for unified content generation and topic management service.
Consolidates both content generation and topic management functionality.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import sqlite3
from pathlib import Path
import logging


def _resolve_log_level() -> int:
    """Resolve log level from environment with safe fallback."""
    level_name = os.getenv('LOG_LEVEL', 'INFO').upper()
    if hasattr(logging, level_name):
        return getattr(logging, level_name)
    logging.warning("Invalid LOG_LEVEL '%s'; defaulting to INFO", level_name)
    return logging.INFO

from .routes_orchestrator import router as orchestrator_router
from .routes_platform import router as platform_router
from .routes_topics import router as topics_router
from .routes_health import router as health_router
from .schemas import HealthResponse


# Configure logging
logging.basicConfig(
    level=_resolve_log_level(),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('content_generation.log'),
        logging.StreamHandler()
    ]
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    setup_database()
    yield
    # Shutdown
    pass


def setup_database():
    """Initialize unified database."""
    # Ensure data directory exists
    data_dir = Path("./data")
    data_dir.mkdir(exist_ok=True)
    
    # Create cache directory
    cache_dir = data_dir / "cache"
    cache_dir.mkdir(exist_ok=True)
    
    # The unified database is already initialized via unified_database.py
    # No need to create separate tables here
    print("✅ Unified database initialized")


# Create FastAPI app
app = FastAPI(
    title="Content Generation API",
    description="Multi-platform content generation service for system design topics",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],  # React dev server
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(orchestrator_router, prefix="/api", tags=["content-generation"])
app.include_router(platform_router, prefix="/api/content", tags=["platform-content"])
app.include_router(topics_router, prefix="/api", tags=["topic-management"])
app.include_router(health_router, tags=["api-health"])


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Unified Content Generation & Topic Management Service",
        "version": "1.0.0",
        "docs": "/docs",
        "features": [
            "Multi-platform content generation",
            "System design topic management", 
            "Real-time processing status",
            "Unified database backend"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
