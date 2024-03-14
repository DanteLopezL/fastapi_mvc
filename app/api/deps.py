from typing import Annotated
from fastapi import Depends
from app.db.database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database dependency injection for query methods
db_dependency = Annotated[Session, Depends(get_db)]