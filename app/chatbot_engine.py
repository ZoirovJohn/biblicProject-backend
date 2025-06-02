from sqlalchemy.orm import Session
from .memory_processor import MemoryProcessor
from . import crud
import logging

logger = logging.getLogger(__name__)

class ChatbotEngine:
    def __init__(self, memory_processor: MemoryProcessor):
        self.memory_processor = memory_processor

    def generate_response(self, user_id: str, message: str, db: Session):
        """Generate contextual response using memories"""
        try:
            # Search for relevant memories
            relevant_memories = self.memory_processor.search_relevant_memories(
                user_id=user_id, 
                query=message, 
                limit=5
            )
            
            # Get recent conversation context
            recent_context = crud.get_conversation_context(db, user_id, limit=5)
            
            # Build context for response
            context_parts = []
            
            if relevant_memories.get("memories"):
                context_parts.append("Relevant memories:")
                for memory in relevant_memories["memories"][:3]:
                    context_parts.append(f"- {memory.get('memory', '')}")
            
            if recent_context:
                context_parts.append("\nRecent conversation context:")
                for ctx in recent_context[:2]:
                    if ctx.metadata.get("last_message"):
                        context_parts.append(f"- {ctx.metadata['last_message']}")
            
            # Generate response (this is a simple example - replace with your AI model)
            context_str = "\n".join(context_parts)
            response = self._generate_ai_response(message, context_str, user_id)
            
            return {
                "response": response,
                "context_used": context_parts,
                "memories_found": len(relevant_memories.get("memories", []))
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "response": "I apologize, but I encountered an error while processing your message.",
                "context_used": [],
                "memories_found": 0
            }

    def _generate_ai_response(self, message: str, context: str, user_id: str) -> str:
        """
        Placeholder for AI response generation
        Replace this with your preferred AI model (OpenAI, Anthropic, etc.)
        """
        if context:
            return f"Based on our previous conversations and what I know about you: I understand you're asking about '{message}'. {context[:200]}... How can I help you further?"
        else:
            return f"I'd be happy to help you with '{message}'. Could you provide more context so I can give you a more personalized response?"