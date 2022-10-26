from email import contentmanager
from turtle import pos
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends


models.Base.metadata.create_all(bind=engine)

app = FastAPI()






   
 #setup the database connection
 #add while loop to keep try the following block for the situations where your internet is disconnected or 
 #the database server is not responding
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='pyapi', user='postgres', password='Ansr1991!',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was succesfull!')
        break
    except Exception as error:
        print('Error with database connection')
        print('Error: ', error)
        # pasue for 2 seconds before executing the server connection
        time.sleep(2)




# request Get method url:"/"
@app.get("/")
def get_user():
    return {"message": "Welcome to my api"}

# request Get method for posts url:"/posts"
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # this only prepares the query string
    # cursor.execute("""SELECT * FROM posts;""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

# latest can be treated as a variable for {id}. the order for path parameters matters
@app.get("/post/latest")
def get_lastest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

@app.get("/post/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id))
    #post = cursor.fetchone()

    post =db.query(models.Post).filter(models.Post.id == id).first()

    if post ==None:
        # change the status code upon an exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                       detail=f"The post with id:{id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"The post with id:{id} not found"}
    return {"post": post}

# change the defaul status code
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #               (post.title, post.content, post.published))
    #new_post=cursor.fetchone()
    ## saving the changes to the database
    #conn.commit()
    
    # this method works if you have a limited number of colums
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    
    # the ** automatically unpacks the dictionary into corresponding fields of the Post model
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    # This is the RETURNING functionality of the SQL
    db.refresh(new_post)
    
    return {"data" : new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit() 
    post_query =db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
          detail=f"post with id:{id} not found")
    
    post_query.delete(synchronize_session=False)
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    
    post_query =db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
          detail=f"post with id:{id} not found")
    # provide a dictionary of the columns and their data to the update method
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
    