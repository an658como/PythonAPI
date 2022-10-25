from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
# setup the database connection

try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Ansr1991!',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('Database connection was succesfull!')
except Exception as error:
    print('Error with database connection')
    print('Error: ', error)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "ID": 1},
            {"title": "favortie foods", "content": "I love pizza", "ID": 2}]

def find_post(id):
    for post in my_posts:
        if post.get("ID") == id:
            return post

def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post.get("ID") == id:
            return i

# request Get method url:"/"
@app.get("/")
def get_user():
    return {"message": "Welcome to my api"}

# request Get method for posts url:"/posts"
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# latest can be treated as a variable for {id}. the order for path parameters matters
@app.get("/post/latest")
def get_lastest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

@app.get("/post/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if post ==None:
        # change the status code upon an exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                       detail=f"The post with id:{id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"The post with id:{id} not found"}
    return {"post": post}

# change the defaul status code
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['ID'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return post_dict

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
          detail=f"post with id:{id} not found")
    my_posts.pop(index)
    return {"message": "post succesfully deleted."}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
          detail=f"post with id:{id} not found")
    post_dict = post.dict()
    post_dict['ID'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}





