from sqlalchemy import Column, String
from pydantic import BaseModel , Field

class UserRequest(BaseModel):
    email  : str= Field(min_length=8)
    username : str = Field(min_length=3)
    first_name : str = Field()
    last_name : str = Field()
    password : str = Field()

class TodoRequest(BaseModel):
    title : str = Field(min_length=3)
    description : str = Field(min_length=3 , max_length=100)
    priority : int = Field(gt=0 , lt=6)
    complete: bool = Field(default=False)
    
class PasswordChangeRequest(BaseModel):
    password : str
    new_password : str = Field(min_length=3)