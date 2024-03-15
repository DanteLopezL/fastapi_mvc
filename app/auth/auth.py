from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import ALGORITHM, SECRET_KEY, db_dependency
from app.models.models import User
from app.models.requests import UserRequest
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from jose import jwt
from datetime import timedelta, datetime, timezone

auth_router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'])

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
async def login_for_access_token( form_data : Annotated[OAuth2PasswordRequestForm, Depends()] , db : db_dependency ):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(f'No user with username : {form_data.username}')
    if not bcrypt_context.verify(form_data.password , user.password):
        raise HTTPException('Incorrect password')
    
    token = create_access_token(user_id=user._id, username=user.username , expires_delta=timedelta(hours=4) , role=user.role)
    return {
        'access_token' : token,
        'token_type' : 'bearer'
    }

@auth_router.post('/new')
async def create_user( db : db_dependency ,request : UserRequest):
    user = User(
        email=request.email,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        password=bcrypt_context.hash(request.password),
        role='mod',
        phone_number = request.phone_number
    )
    db.add(user)
    db.commit()
    return f'Successfully created user'