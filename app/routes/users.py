from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, models
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/user/{user_id}/profile")
async def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    """Get user profile based on stored memories"""
    try:
        # Get all long-term memories
        memories = db.query(models.Memory).filter(
            models.Memory.user_id == user_id,
            models.Memory.is_long_term == True
        ).all()
        
        # Get conversation stats
        conversations = db.query(models.Memory).filter(
            models.Memory.user_id == user_id,
            models.Memory.metadata.contains({"type": "conversation"})
        ).count()
        
        # Build profile
        profile = {
            "user_id": user_id,
            "total_memories": len(memories),
            "total_conversations": conversations,
            "first_interaction": memories[-1].created_at if memories else None,
            "last_interaction": memories[0].created_at if memories else None,
            "key_memories": [m.content for m in memories[:5]]
        }
        
        return {"status": "success", "profile": profile}
        
    except Exception as e:
        logger.error(f"Profile error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))