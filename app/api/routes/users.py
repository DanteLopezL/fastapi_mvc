from fastapi import APIRouter, HTTPException, Query, status
from app.api.deps import db_dependency , user_dependency
from app.models.models import User
from app.auth.auth import bcrypt_context
from app.models.requests import PasswordChangeRequest, UserRequest

user_router = APIRouter()

@user_router.get('/get')
async def get_user( db : db_dependency , user : user_dependency ):
    return db.query(User).filter(User._id == user.get('user_id')).first()

@user_router.put('/edit/password')
async def change_user_password( db : db_dependency , user : user_dependency , request : PasswordChangeRequest):
    found_user = db.query(User).filter(User._id == user.get('user_id')).first()
    if not bcrypt_context.verify( request.password , user.password ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    found_user.password = bcrypt_context.hash(request.new_password)
    db.add(found_user)
    db.commit()
    return 'Successfully edited password'

@user_router.put('/edit/phonenumber')
async def update_user_phone_number( db : db_dependency, user : user_dependency , phone_number = Query(min_length=9) ):
    found_user = db.query(User).filter(User._id == user.get('user_id')).first()
    found_user.phone_number = phone_number
    db.add(found_user)
    db.commit()
    return f'Phone number {phone_number} successfully edited'