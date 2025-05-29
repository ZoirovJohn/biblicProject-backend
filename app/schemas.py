from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class MemoryCreate(BaseModel):
    user_id: str
    content: str
    metadata: Optional[Dict] = {}
    is_long_term: Optional[bool] = False

class MemoryOut(MemoryCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
