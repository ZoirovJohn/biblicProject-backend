from sqlalchemy.orm import Session
from . import models, schemas

def create_memory(db: Session, memory_data: schemas.MemoryCreate):
    db_memory = models.Memory(**memory_data.dict())
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory
