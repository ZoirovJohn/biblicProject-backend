from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..schemas import ConversationInput, MemorySearchInput
from ..memory_processor import MemoryProcessor
from .. import crud
from mem0 import MemoryClient
import logging
import os

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize components
os.environ['MEM0_API_KEY'] = 'm0-KiyeA4o0sgUE7119FmpBWuUtVO0JgGflARKgIhQu'
client = MemoryClient()
memory_processor = MemoryProcessor(client)

@router.post("/process-conversation")
async def process_conversation(
    data: ConversationInput,
    db: Session = Depends(get_db)
):
    """Process a full conversation and extract memories"""
    try:
        if not data.messages:
            raise HTTPException(status_code=400, detail="No messages provided")
        
        result = memory_processor.extract_and_store_memories(
            user_id=data.user_id,
            messages=data.messages,
            db=db
        )
        
        return {
            "status": "success",
            "extracted_memories_count": len(result["extracted_memories"]),
            "mem0_result": result["mem0_result"],
            "conversation_stored": True
        }
        
    except Exception as e:
        logger.error(f"Conversation processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search-memories")
async def search_memories(data: MemorySearchInput):
    """Enhanced memory search"""
    try:
        result = memory_processor.search_relevant_memories(
            user_id=data.user_id,
            query=data.query,
            limit=data.limit
        )
        
        return {
            "status": "success",
            "query": data.query,
            "results": result.get("memories", []),
            "total_found": len(result.get("memories", []))
        }
        
    except Exception as e:
        logger.error(f"Memory search error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}/memories")
async def get_user_memories(
    user_id: str,
    limit: int = 50,
    memory_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get user's stored memories with filtering"""
    try:
        memories = crud.get_user_memories(db, user_id, limit, memory_type)
        
        return {
            "status": "success",
            "user_id": user_id,
            "memories": [
                {
                    "id": m.id,
                    "content": m.content,
                    "metadata": m.metadata,
                    "is_long_term": m.is_long_term,
                    "created_at": m.created_at
                } for m in memories
            ],
            "total": len(memories)
        }
        
    except Exception as e:
        logger.error(f"Get memories error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/user/{user_id}/memories")
async def delete_user_memories(
    user_id: str,
    memory_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Delete user memories with optional filtering"""
    try:
        query = db.query(models.Memory).filter(models.Memory.user_id == user_id)
        
        if memory_type:
            query = query.filter(models.Memory.metadata.contains({"type": memory_type}))
        
        deleted_count = query.count()
        query.delete(synchronize_session=False)
        db.commit()
        
        # Also delete from mem0
        try:
            filters = {"AND": [{"user_id": user_id}]}
            client.delete_all(filters=filters)
        except Exception as mem0_error:
            logger.warning(f"Failed to delete from mem0: {mem0_error}")
        
        return {
            "status": "success",
            "deleted_count": deleted_count,
            "user_id": user_id
        }
        
    except Exception as e:
        logger.error(f"Delete memories error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))