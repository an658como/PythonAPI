from email.quoprimime import body_check
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "ID": 1},
            {"title": "favortie foods", "content": "I love pizza", "ID": 2}]



# request Get method url:"/"
@app.get("/")
def get_user():
    return {"message": "Welcome to my api"}

# request Get method for posts url:"/posts"
@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):
    print(post)
    print(post.dict())
    return{"data": "new_post"}
