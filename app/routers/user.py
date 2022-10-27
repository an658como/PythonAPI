from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import get_db


router=APIRouter(
    prefix='/users',
    tags = ['users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    user.password = utils.hash(user.password)
    
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    # This is the RETURNING functionality of the SQL
    db.refresh(new_user)
    # The class config setting in the schema allows the  automatic conversion of new_post (SQLAlchemy) to the the chosen response model (Dictionary)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).one()
    
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    
    return user