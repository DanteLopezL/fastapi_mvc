from fastapi import APIRouter, Query
from app.api.deps import db_dependency , user_dependency

user_router = APIRouter()

@user_router.get('/get')
async def get_user( db : db_dependency , user : user_dependency , id: int = Query(gt=0)):
    return