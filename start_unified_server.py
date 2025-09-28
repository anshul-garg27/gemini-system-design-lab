#!/usr/bin/env python3
"""
Start the unified FastAPI server.
This replaces both Flask and FastAPI servers with a single unified server.
"""
import uvicorn
import os
from pathlib import Path

# Set environment variables
os.environ.setdefault('GEMINI_API_KEY', 'your-api-key-here')
os.environ.setdefault('LOG_LEVEL', 'DEBUG')

if __name__ == "__main__":
    print("🚀 Starting Unified FastAPI Server...")
    print("📊 Features:")
    print("  ✅ Multi-platform content generation")
    print("  ✅ System design topic management")
    print("  ✅ Real-time processing status")
    print("  ✅ Unified database backend")
    print("  ✅ React frontend support")
    print()
    print("🌐 Server will be available at:")
    print("  📱 Frontend: http://localhost:5173")
    print("  🔧 API: http://localhost:8000")
    print("  📚 Docs: http://localhost:8000/docs")
    print()
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )
