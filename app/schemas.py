from datetime import datetime
from pydantic import BaseModel

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
    # Be cautious this response is supposed to work with SQLAlchemy while pydantic only understand dictionaries
    # The following config setting allows SQLAlchemy data work as a dictionary
    class Config:
        orm_mode = True