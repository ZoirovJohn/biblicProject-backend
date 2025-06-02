from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models, schemas
from typing import List, Optional

def create_memory(db: Session, memory_data: schemas.MemoryCreate):
    """Create a single memory"""
    db_memory = models.Memory(**memory_data.dict())
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory

def create_memory_batch(db: Session, memories: List[schemas.MemoryCreate]):
    """Create multiple memories in batch"""
    db_memories = []
    for memory_data in memories:
        db_memory = models.Memory(**memory_data.dict())
        db.add(db_memory)
        db_memories.append(db_memory)
    
    db.commit()
    for memory in db_memories:
        db.refresh(memory)
    return db_memories

def get_user_memories(db: Session, user_id: str, limit: int = 50, memory_type: Optional[str] = None):
    """Get user memories with optional filtering"""
    query = db.query(models.Memory).filter(models.Memory.user_id == user_id)
    
    if memory_type:
        query = query.filter(models.Memory.meta_data.contains({"type": memory_type}))
    
    return query.order_by(desc(models.Memory.created_at)).limit(limit).all()

def get_conversation_context(db: Session, user_id: str, limit: int = 10):
    """Get recent conversation context"""
    return db.query(models.Memory).filter(
        models.Memory.user_id == user_id,
        models.Memory.metadata.contains({"type": "conversation"})
    ).order_by(desc(models.Memory.created_at)).limit(limit).all()

def create_conversation_session(db: Session, session_data: schemas.ConversationSessionCreate):
    """Create a new conversation session"""
    db_session = models.ConversationSession(**session_data.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def create_user_profile(db: Session, profile_data: schemas.UserProfileCreate):
    """Create a new user profile"""
    db_profile = models.UserProfile(**profile_data.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_user_profile(db: Session, user_id: str):
    """Get user profile by user_id"""
    return db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()

def update_user_profile_stats(db: Session, user_id: str, conversations_increment: int = 0, memories_increment: int = 0):
    """Update user profile statistics"""
    profile = get_user_profile(db, user_id)
    if profile:
        profile.total_conversations += conversations_increment
        profile.total_memories += memories_increment
        profile.last_interaction = models.datetime.utcnow()
        db.commit()
        db.refresh(profile)
    return profile