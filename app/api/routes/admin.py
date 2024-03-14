from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.deps import db_dependency
from app.models.requests import TodoRequest
from app.models.models import Todo
from app.auth.auth import get_current_user

admin_router = APIRouter()

user_dependency = Annotated[dict , Depends(get_current_user)]

@admin_router.get('/todos/all')
async def get_all_todos( db : db_dependency , user : user_dependency ):
    if user.get('role') is not 'admin':
        raise HTTPException(status_code=401, detail='Invalid cedentials')
    return db.query(Todo).all()