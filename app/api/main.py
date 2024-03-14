from fastapi import APIRouter
from app.api.routes.todos import todo_router
from app.auth.auth import auth_router

router = APIRouter()

router.include_router( auth_router , prefix='/auth' ,tags=['auth']  )
router.include_router( todo_router , prefix='/todos' , tags=['todos'])