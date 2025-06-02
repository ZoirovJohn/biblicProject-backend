from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
from datetime import datetime
import uuid

class Memory(Base):
    __tablename__ = "memories"  # FIXED: Was missing underscores

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True, nullable=False)
    content = Column(Text, nullable=False)
    meta_data = Column(JSON, default={})  # Renamed from 'metadata'
    is_long_term = Column(Boolean, default=False, index=True)
    confidence_score = Column(Float, default=0.0)
    mem0_id = Column(String(255), index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ConversationSession(Base):
    __tablename__ = "conversation_sessions"  # FIXED: Was missing underscores

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(255), index=True, nullable=False)
    title = Column(String(500), nullable=True)
    message_count = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    session_meta = Column(JSON, default={})  # Renamed from 'metadata'

class UserProfile(Base):
    __tablename__ = "user_profiles"  # FIXED: Was missing underscores

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), unique=True, index=True, nullable=False)
    display_name = Column(String(255), nullable=True)
    preferences = Column(JSON, default={})
    total_conversations = Column(Integer, default=0)
    total_memories = Column(Integer, default=0)
    first_interaction = Column(DateTime, default=datetime.utcnow)
    last_interaction = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)