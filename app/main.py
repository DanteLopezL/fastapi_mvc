from fastapi import FastAPI
from app.api.main import router
from app.db.database import engine
from app.models.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
