from fastapi import APIRouter, Depends, HTTPException , status
from app.api.deps import db_dependency
from app.models.models import User
from app.models.requests import UserRequest
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone

auth_router = APIRouter()

SECRET_KEY = 'bG9yZHJhbmRhcnNhcmFz'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')

def create_access_token(username : str , user_id : int , expires_delta : timedelta):
    encode = {
        'sub': username,
        'id': user_id,
        'exp' : datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(
        encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

async def get_current_user(token : Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
        return {
            'username' : username,
            'user_id': user_id
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

@auth_router.get('/details/get')
async def get_user_details():
    return 'Authenticated'

@auth_router.post('/new')
async def create_user( db : db_dependency ,request : UserRequest):
    user = User(
        email=request.email,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        password=bcrypt_context.hash(request.password),
        role='mod'
    )
    db.add(user)
    db.commit()
    return f'Successfully created user'

@auth_router.post('/token')
async def login_for_access_token( form_data : Annotated[OAuth2PasswordRequestForm, Depends()] , db : db_dependency ):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(f'No user with username : {form_data.username}')
    if not bcrypt_context.verify(form_data.password , user.password):
        raise HTTPException('Incorrect password')
    
    token = create_access_token(user_id=user._id, username=user.username , expires_delta=timedelta(hours=4))
    return token