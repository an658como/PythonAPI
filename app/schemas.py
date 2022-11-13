from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# The same way you define a model for your data to be received from the client, you can
# define a model for the response

class Post(PostBase):
    # There is no reason to include title, etc. because of the inheritance
    id: int
    created_at: datetime
    owner_id: int
    # Be cautious this response is supposed to work with SQLAlchemy while pydantic only understand dictionaries
    # The following config setting allows SQLAlchemy data work as a dictionary
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    # The emailvalidator library is already installed
    # Pydantic has data type which makes sure your email address is entered properly EmailStr
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None