from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from app.api.deps import ALGORITHM, SECRET_KEY, db_dependency
from app.models.models import User
from app.models.requests import UserRequest
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Optional
from jose import jwt
from datetime import timedelta, datetime, timezone

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

auth_router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'])

templates_directory = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_directory))

#################### MVC VERSION #############################
class LoginForm:
    def __init__(self, request : Request) -> None:
        self.request = request
        self.username : Optional[str] = None
        self.password : Optional[str] = None
        
    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get('email')
        self.password = form.get('password')
        

def create_access_token(username : str , role : str , user_id : int , expires_delta : timedelta):
    encode = {
        'sub': username,
        'id': user_id,
        'role' : role,
        'exp' : datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(
         encode,
         SECRET_KEY,
         algorithm=ALGORITHM
     )

@auth_router.post('/token')
async def login_for_access_token( response : Response, form_data : Annotated[OAuth2PasswordRequestForm, Depends()] , db : db_dependency ):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        return False
    if not bcrypt_context.verify(form_data.password , user.password):
        raise HTTPException('Incorrect password')
    
    token = create_access_token(user_id=user._id, username=user.username , expires_delta=timedelta(hours=4) , role=user.role)
    
    response.set_cookie(key='access_token', value=token, httponly=True)
    return True
    # return {
    #     'access_token' : token,
    #     'token_type' : 'bearer'
    # }

@auth_router.get('/login', response_class=HTMLResponse)
async def view_login( request : Request ):
    return templates.TemplateResponse('login.html', { 'request': request })

@auth_router.post('/login' , response_class=HTMLResponse)
async def login( request : Request, db : db_dependency ):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)
        validate_user_cookie = await login_for_access_token(response=response, form_data=form, db=db)
        
        if not validate_user_cookie:
            return templates.TemplateResponse('login.html', { 'request' : request , 'msg': 'Incorrect username or password' })
        return response
    except HTTPException as e:
        return templates.TemplateResponse('login.html', { 'request' : request , 'msg': f'Error {e}' })

@auth_router.get('/register', response_class=HTMLResponse)
async def login( request : Request ):
    return templates.TemplateResponse('register.html', { 'request': request })
        
        
#################### REST VERSION #############################


# @auth_router.get('/login', response_class=HTMLResponse)
# async def login( request : Request ):
#     return templates.TemplateResponse('login.html', { 'request': request })

# @auth_router.get('/register', response_class=HTMLResponse)
# async def login( request : Request ):
#     return templates.TemplateResponse('register.html', { 'request': request })

# def create_access_token(username : str , role : str , user_id : int , expires_delta : timedelta):
#     encode = {
#         'sub': username,
#         'id': user_id,
#         'role' : role,
#         'exp' : datetime.now(timezone.utc) + expires_delta
#     }
#     return jwt.encode(
#         encode,
#         SECRET_KEY,
#         algorithm=ALGORITHM
#     )

# @auth_router.post('/token')
# async def login_for_access_token( form_data : Annotated[OAuth2PasswordRequestForm, Depends()] , db : db_dependency ):
#     user = db.query(User).filter(User.username == form_data.username).first()
#     if not user:
#         raise HTTPException(f'No user with username : {form_data.username}')
#     if not bcrypt_context.verify(form_data.password , user.password):
#         raise HTTPException('Incorrect password')
    
#     token = create_access_token(user_id=user._id, username=user.username , expires_delta=timedelta(hours=4) , role=user.role)
#     return {
#         'access_token' : token,
#         'token_type' : 'bearer'
#     }

# @auth_router.post('/new')
# async def create_user( db : db_dependency ,request : UserRequest):
#     user = User(
#         email=request.email,
#         username=request.username,
#         first_name=request.first_name,
#         last_name=request.last_name,
#         password=bcrypt_context.hash(request.password),
#         role='mod',
#         phone_number = request.phone_number
#     )
#     db.add(user)
#     db.commit()
#     return f'Successfully created user'