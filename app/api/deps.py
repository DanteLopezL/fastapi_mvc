from pathlib import Path
from typing import Annotated
from fastapi import Depends, HTTPException, Request , status
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from jose import JWTError , jwt
from app.db.database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')

SECRET_KEY = 'bG9yZHJhbmRhcnNhcmFz'
ALGORITHM = 'HS256'

templates_directory = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_directory))

async def get_current_user(request : Request):
    try:
        token = request.cookies.get('access_token')
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        role : str = payload.get('role')
        
        if username is None or user_id is None:
            msg = 'Expired token'
            response = templates.TemplateResponse('login.html', { 'request' : request , 'msg' : msg })
            response.delete_cookie(key='access_token')
        
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
        return {
            'username' : username,
            'user_id': user_id,
            'role' : role
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

# async def get_current_user(token : Annotated[str, Depends(oauth2_bearer)]):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username : str = payload.get('sub')
#         user_id : int = payload.get('id')
#         role : str = payload.get('role')
#         if username is None or user_id is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
#         return {
#             'username' : username,
#             'user_id': user_id,
#             'role' : role
#         }
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

# Database dependency injection for query methods
db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict , Depends(get_current_user)]