from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from app import models, schemas, oauth2
from app.database import get_db
from typing import List, Optional



router = APIRouter(
    prefix='/posts',
    tags=['posts']
)

# previously most of path operations were referred as @app. 
# but now app is not included here. Instead of importing app
# to this file, we can define an oject called router and 
# assign the path operations to the router, and finally,
# import the routers to the app in the main file. 

# request Get method for posts url:"/posts"
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_crruent_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    # add a query parameter to your route. Pass the value using /?limit=3
    print("Print the query parameter", limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_crruent_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id))
    #post = cursor.fetchone()

    post =db.query(models.Post).filter(models.Post.id == id).first()

    if post ==None:
        # change the status code upon an exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                       detail=f"The post with id:{id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"The post with id:{id} not found"}

    
    return post

# change the defaul status code
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_crruent_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #               (post.title, post.content, post.published))
    #new_post=cursor.fetchone()
    ## saving the changes to the database
    #conn.commit()
    
    # this method works if you have a limited number of colums
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    
    # the ** automatically unpacks the dictionary into corresponding fields of the Post model

    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    # This is the RETURNING functionality of the SQL
    db.refresh(new_post)
    # The class config setting in the schema allows the  automatic conversion of new_post (SQLAlchemy) to the the chosen response model (Dictionary)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_crruent_user)):

    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit() 
    post_query =db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
          detail=f"post with id:{id} not found")
        
    post = post_query.first()
    print("ID Chekc", post.id, current_user.id)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested actions")
        
    
    post_query.delete(synchronize_session=False)
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_crruent_user)):
    #cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    
    post_query =db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
          detail=f"post with id:{id} not found")
    # provide a dictionary of the columns and their data to the update method

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested actions")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()