from pathlib import Path
from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request, status
from app.api.deps import db_dependency, get_current_user , user_dependency
from app.models.requests import TodoRequest
from app.models.models import Todo

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

todo_router = APIRouter()

templates_directory = Path(__file__).parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_directory))

#################### FULLSTACK VERSION #############################

@todo_router.get('/', response_class=HTMLResponse)
async def view_get_all_by_user( request : Request , db : db_dependency ):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth/login', status_code=status.HTTP_302_FOUND)
    todos = db.query(Todo).filter(Todo.user_id == user.get('user_id'), Todo.complete == False).all()
    return templates.TemplateResponse('home.html', { 'request': request , 'todos' : todos , 'user' : user })

@todo_router.get('/new', response_class=HTMLResponse)
async def view_create_new_todo( request : Request ):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth/login', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('add-todo.html', { 'request': request , 'user' : user })

@todo_router.post('/new')
async def create_new_todo( request : Request,  db : db_dependency , title : str = Form(...) , description : str = Form(...) , priority : int = Form(...)):
    user = await get_current_user(request)
    todo = Todo()
    todo.title = title
    todo.description = description
    todo.priority = priority
    todo.complete = False
    todo.user_id = user.get('user_id')
    db.add(todo)
    db.commit()
    
    return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)

@todo_router.get('/edit', response_class=HTMLResponse)
async def view_edit_todo( request : Request , db : db_dependency , todo_id : int = Query(...) ):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth/login', status_code=status.HTTP_302_FOUND)
    todo = db.query(Todo).filter(Todo._id == todo_id).first()
    
    return templates.TemplateResponse('edit-todo.html', { 'request': request , 'todo': todo , 'user' : user})

@todo_router.post('/edit', response_class=HTMLResponse)
async def edit_todo( request : Request , db : db_dependency , todo_id : int = Query(...) , title = Form(...) , description = Form(...) , priority = Form(...) ):
    todo = db.query(Todo).filter(Todo._id == todo_id).first()
    
    todo.title = title
    todo.description = description
    todo.priority = priority
    
    db.add(todo)
    db.commit()
    
    return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)

@todo_router.get('/delete')
async def delete_todo( request : Request, db : db_dependency, todo_id: int = Query(...) ):
    todo = db.query(Todo).filter(Todo._id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail=f'Not such todo with id {id}')
    
    db.query(Todo).filter(Todo._id == todo_id).delete()
    db.commit()
    return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)

@todo_router.get('/complete')
async def complete_todo( request : Request , db : db_dependency , todo_id = Query(...) ):
    todo = db.query(Todo).filter(Todo._id == todo_id).first()
    todo.complete = True
    db.add(todo)
    db.commit()
    return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)

#################### REST VERSION #############################

# @todo_router.get('/get')
# async def get_todo_by_id( user : user_dependency, db : db_dependency , id: int = Query(gt=0) ):
#     todo = db.query(Todo).filter(Todo.id_ == id).first()
#     if todo is not None:
#         return todo
#     raise HTTPException(status_code=404 , detail='Todo does not exist')

# @todo_router.post('/new')
# async def create_new_todo( user : user_dependency, db : db_dependency, request : TodoRequest ):
#     todo = Todo(**request.model_dump(), user_id= user.get('user_id'))
#     db.add(todo)
#     db.commit()
#     return 'Successfully created todo'

# @todo_router.put('/edit')
# async def edit_todo( user : user_dependency, db : db_dependency , request : TodoRequest , id: int = Query(gt=0) ):
#     todo = db.query(Todo).filter(Todo.id_ == id).filter(Todo.user_id == user.get('user_id')).first()
#     if todo is None:
#         raise HTTPException(status_code=404, detail=f'Not such todo with id {id}')
#     todo.title = request.title
#     todo.description = request.description
#     todo.priority = request.priority
#     todo.complete = request.complete
    
#     db.add(todo)
#     db.commit()
    
#     return f'Todo successfully edited'

# @todo_router.delete('/delete')
# async def delete_todo( user : user_dependency, db : db_dependency, id: int = Query(gt=0) ):
#     todo = db.query(Todo).filter(Todo.id_ == id).first()
#     if todo is None:
#         raise HTTPException(status_code=404, detail=f'Not such todo with id {id}')
    
#     db.query(Todo).filter(Todo.id_ == id).delete()
#     db.commit()
#     return 'Todo successfully deleted'

# @todo_router.get('/all')
# async def get_all_todos(db: db_dependency, user : user_dependency):
#     return db.query(Todo).filter(Todo.user_id == user.get('user_id')).all()