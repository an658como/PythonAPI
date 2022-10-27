from fastapi import APIRouter, HTTPException, Response, Depends, status
from sqlalchemy.orm import Session
from app.schemas import UserLogin

from app.database import get_db
from app import models
from app.utils import verify

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: UserLogin,  db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='Invalid Credintials')
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='Invalid Credintials') 
        
    # create token     
    return {"token": "example token"}
