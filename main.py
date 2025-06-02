from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from app.routes import chat, memories, users
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(title="AI Chatbot with Memory", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables
models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(memories.router, prefix="/api", tags=["Memories"])
app.include_router(users.router, prefix="/api", tags=["Users"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Chatbot with Memory API",
        "version": "2.0.0",
        "timestamp": datetime.utcnow()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "2.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)