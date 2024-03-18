from fastapi import FastAPI , status
from fastapi.responses import RedirectResponse
from app.api.main import router
from app.db.database import engine
from app.models.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
async def root():
    return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)

app.include_router(router)
