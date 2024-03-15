from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.deps import db_dependency , user_dependency
from app.models.requests import TodoRequest
from app.models.models import Todo

todo_router = APIRouter()

@todo_router.get('/get')
async def get_todo_by_id( user : user_dependency, db : db_dependency , id: int = Query(gt=0) ):
    todo = db.query(Todo).filter(Todo.id_ == id).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=404 , detail='Todo does not exist')

@todo_router.post('/new')
async def create_new_todo( user : user_dependency, db : db_dependency, request : TodoRequest ):
    todo = Todo(**request.model_dump(), user_id= user.get('user_id'))
    db.add(todo)
    db.commit()
    return 'Successfully created todo'

@todo_router.put('/edit')
async def edit_todo( user : user_dependency, db : db_dependency , request : TodoRequest , id: int = Query(gt=0) ):
    todo = db.query(Todo).filter(Todo.id_ == id).filter(Todo.user_id == user.get('user_id')).first()
    if todo is None:
        raise HTTPException(status_code=404, detail=f'Not such todo with id {id}')
    todo.title = request.title
    todo.description = request.description
    todo.priority = request.priority
    todo.complete = request.complete
    
    db.add(todo)
    db.commit()
    
    return f'Todo successfully edited'

@todo_router.delete('/delete')
async def delete_todo( user : user_dependency, db : db_dependency, id: int = Query(gt=0) ):
    todo = db.query(Todo).filter(Todo.id_ == id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail=f'Not such todo with id {id}')
    
    db.query(Todo).filter(Todo.id_ == id).delete()
    db.commit()
    return 'Todo successfully deleted'

@todo_router.get('/all')
async def get_all_todos(db: db_dependency, user : user_dependency):
    return db.query(Todo).filter(Todo.user_id == user.get('user_id')).all()