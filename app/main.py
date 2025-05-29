from fastapi import FastAPI, Depends
from pydantic import BaseModel
from mem0 import MemoryClient
from sqlalchemy.orm import Session
from app import models, database, crud, schemas
import os

# Initialize env and Mem0
os.environ['MEM0_API_KEY'] = 'm0-KiyeA4o0sgUE7119FmpBWuUtVO0JgGflARKgIhQu'
client = MemoryClient()

# FastAPI app
app = FastAPI()

# Auto-create DB tables
models.Base.metadata.create_all(bind=database.engine)

# ---- MEM0 INPUT CLASSES ----

class MemoryInput(BaseModel):
    user_id: str
    memory: list  # List of {"role": ..., "content": ...}

class SearchInput(BaseModel):
    user_id: str
    query: str

# ---- MEM0 ROUTES ----

@app.post("/add-memory")
def add_memory(
    data: MemoryInput,
    db: Session = Depends(database.SessionLocal)
):
    # 1. Send to Mem0
    mem0_result = client.add(messages=data.memory, user_id=data.user_id)

    # 2. Parse Mem0 response (basic)
    for message in data.memory:
        content = message["content"]
        metadata = {"mem0_id": mem0_result["memories"][0]["id"]}  # You can loop if multiple memories
        crud.create_memory(db, schemas.MemoryCreate(
            user_id=data.user_id,
            content=content,
            metadata=metadata,
            is_long_term=False  # or set from input if needed
        ))

    return {
        "status": "success",
        "mem0_result": mem0_result,
        "db_status": "synced"
    }


@app.post("/search-memory")
def search_memory(data: SearchInput):
    filters = {"AND": [{"user_id": data.user_id}]}
    result = client.search(data.query, version="v2", filters=filters)
    return {"status": "success", "result": result}

@app.get("/get-all-memories/{user_id}")
def get_all_memories(user_id: str):
    filters = {"AND": [{"user_id": user_id}]}
    result = client.get_all(version="v2", filters=filters)
    return {"status": "success", "result": result}

@app.post("/save-memory-db", response_model=schemas.MemoryOut)
def save_memory(memory: schemas.MemoryCreate, db: Session = Depends(database.SessionLocal)):
    return crud.create_memory(db, memory)
