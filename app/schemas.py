from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


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
        from_attribute = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


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
    owner: UserOut

    # Be cautious this response is supposed to work with SQLAlchemy while pydantic only understand dictionaries
    # The following config setting allows SQLAlchemy data work as a dictionary
    class Config:
        from_attribute = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attribute = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # you just need a datatype that can provde only 0 and 1
