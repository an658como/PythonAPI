from fastapi import FastAPI
from . import models
from .database import engine
from app.routers import post, user, auth, vote
from .config import settings


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# instead of including all of our path operations in the main file,
# users and posts path operations were moved to seperate files.
# the concept router is required to replace @app with @router in the
# seperated files to refer to the app. post.router and user.router are the
# objects that include the path operations.
# Here we only include the path operations into app.

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# request Get method url:"/"
@app.get("/")
def get_user():
    return {"message": "Welcome to my api"}
