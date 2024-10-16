from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schemas, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from sqlalchemy.orm import Session
from .config import settings

# define your password endpoint object
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# SECRET_KEY
# Algorithm
# Expiration time of the token

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    # make a copy of the passed data
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_crruent_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credintials_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Could not validate credintials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credintials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
