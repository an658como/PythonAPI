from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# If you want to communicate with your database, you need to have a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Any models or tables you are creating is going to be an extension of this base class
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()