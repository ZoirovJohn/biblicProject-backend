from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import ChatInput, ChatMessage
from ..memory_processor import MemoryProcessor
from ..chatbot_engine import ChatbotEngine
from mem0 import MemoryClient
import logging
import os

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize components
os.environ['MEM0_API_KEY'] = 'm0-KiyeA4o0sgUE7119FmpBWuUtVO0JgGflARKgIhQu'
client = MemoryClient()
memory_processor = MemoryProcessor(client)
chatbot_engine = ChatbotEngine(memory_processor)

@router.post("/chat")
async def chat_with_bot(
    data: ChatInput,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Main chat endpoint with memory integration"""
    try:
        # Generate response
        response_data = chatbot_engine.generate_response(
            user_id=data.user_id,
            message=data.message,
            db=db
        )
        
        # Store this interaction in background
        if data.include_context:
            messages = [
                ChatMessage(role="user", content=data.message),
                ChatMessage(role="assistant", content=response_data["response"])
            ]
            background_tasks.add_task(
                memory_processor.extract_and_store_memories,
                data.user_id,
                messages,
                db
            )
        
        return {
            "status": "success",
            "response": response_data["response"],
            "context_used": response_data["context_used"],
            "memories_found": response_data["memories_found"]
        }
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))