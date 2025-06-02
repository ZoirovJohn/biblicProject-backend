from mem0 import MemoryClient
from sqlalchemy.orm import Session
from . import crud, schemas
from .schemas import ChatMessage
from typing import List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MemoryProcessor:
    def __init__(self, mem0_client: MemoryClient):
        self.client = mem0_client

    def extract_and_store_memories(self, user_id: str, messages: List[ChatMessage], db: Session):
        """Enhanced memory extraction and storage"""
        try:
            # Convert messages for mem0
            mem0_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
            
            # Extract memories using mem0
            mem0_result = self.client.add(messages=mem0_messages, user_id=user_id)
            
            # Store in local database with enhanced metadata
            db_memories = []
            if mem0_result.get("memories"):
                for i, memory in enumerate(mem0_result["memories"]):
                    memory_create = schemas.MemoryCreate(
                        user_id=user_id,
                        content=memory.get("memory", ""),
                        metadata={
                            "mem0_id": memory.get("id"),
                            "type": "extracted_memory",
                            "confidence": memory.get("score", 0),
                            "source_messages": len(messages),
                            "extraction_timestamp": datetime.utcnow().isoformat()
                        },
                        is_long_term=True,
                        mem0_id=memory.get("id"),
                        confidence_score=memory.get("score", 0)
                    )
                    db_memory = crud.create_memory(db, memory_create)
                    db_memories.append(db_memory)

            # Also store conversation for context
            conversation_summary = f"Conversation with {len(messages)} messages"
            conversation_memory = schemas.MemoryCreate(
                user_id=user_id,
                content=conversation_summary,
                metadata={
                    "type": "conversation",
                    "message_count": len(messages),
                    "last_message": messages[-1].content[:100] if messages else "",
                    "timestamp": datetime.utcnow().isoformat()
                },
                is_long_term=False
            )
            db_conversation = crud.create_memory(db, conversation_memory)
            
            # Update user profile stats
            crud.update_user_profile_stats(db, user_id, conversations_increment=1, memories_increment=len(db_memories))
            
            return {
                "extracted_memories": db_memories,
                "conversation_record": db_conversation,
                "mem0_result": mem0_result
            }
            
        except Exception as e:
            logger.error(f"Error in memory extraction: {str(e)}")
            raise Exception(f"Memory extraction failed: {str(e)}")

    def search_relevant_memories(self, user_id: str, query: str, limit: int = 10):
        """Search for relevant memories"""
        try:
            filters = {"AND": [{"user_id": user_id}]}
            result = self.client.search(query, version="v2", filters=filters, limit=limit)
            return result
        except Exception as e:
            logger.error(f"Error in memory search: {str(e)}")
            return {"memories": []}