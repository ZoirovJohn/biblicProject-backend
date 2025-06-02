from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class MemoryCreate(BaseModel):
    user_id: str
    content: str
    meta_data: Optional[Dict[str, Any]] = {}  # FIXED: Changed from metadata to meta_data
    is_long_term: Optional[bool] = False
    confidence_score: Optional[float] = 0.0
    mem0_id: Optional[str] = None

class MemoryOut(BaseModel):
    id: int
    user_id: str
    content: str
    meta_data: Dict[str, Any]  # FIXED: Changed from metadata to meta_data
    is_long_term: bool
    confidence_score: float
    mem0_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ConversationSessionCreate(BaseModel):
    user_id: str
    title: Optional[str] = None
    session_meta: Optional[Dict[str, Any]] = {}  # FIXED: Changed from metadata to session_meta

class ConversationSessionOut(BaseModel):
    id: int
    session_id: str
    user_id: str
    title: Optional[str]
    message_count: int
    started_at: datetime
    last_activity: datetime
    session_meta: Dict[str, Any]  # FIXED: Changed from metadata to session_meta

    class Config:
        orm_mode = True

# Rest of your schemas remain the same...
class UserProfileCreate(BaseModel):
    user_id: str
    display_name: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = {}

class UserProfileOut(BaseModel):
    id: int
    user_id: str
    display_name: Optional[str]
    preferences: Dict[str, Any]
    total_conversations: int
    total_memories: int
    first_interaction: datetime
    last_interaction: datetime
    is_active: bool

    class Config:
        orm_mode = True

# API Input Models remain the same...
class ChatMessage(BaseModel):
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = None

class ConversationInput(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    messages: List[ChatMessage] = Field(..., description="Conversation messages")
    extract_memories: bool = Field(True, description="Whether to extract and store memories")
    context_window: int = Field(10, description="Number of recent messages to consider")

class MemorySearchInput(BaseModel):
    user_id: str
    query: str
    limit: int = Field(10, description="Maximum number of results")
    include_metadata: bool = Field(True, description="Include memory metadata")

class ChatInput(BaseModel):
    user_id: str
    message: str
    include_context: bool = Field(True, description="Include relevant memories in response")