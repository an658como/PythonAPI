from fastapi import APIRouter, HTTPException, Response, Depends, status
from sqlalchemy.orm import Session
from app import schemas
from app.schemas import UserLogin

# Import the password request form instead of using your own data model
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.database import get_db
from app import models, oauth2
from app.utils import verify


router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    # Using OAuth2Passwrod form, there is no dedicated email field. The email is stored in the username
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credintials"
        )

    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credintials"
        )

    # create token

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
