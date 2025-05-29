from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from .database import Base
from datetime import datetime

class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    content = Column(String)
    metadata = Column(JSON)
    is_long_term = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
