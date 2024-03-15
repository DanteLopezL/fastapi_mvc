from fastapi import APIRouter, HTTPException
from app.api.deps import db_dependency , user_dependency
from app.models.models import Todo

admin_router = APIRouter()

@admin_router.get('/todos/all')
async def get_all_todos( db : db_dependency , user : user_dependency ):
    if user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Invalid cedentials')
    return db.query(Todo).all()