from contextlib import nullcontext
from email.policy import default
from enum import unique
from .database import Base
# import a package for columns and datatypes 
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP


class Post(Base):
    # Table name in postgres
    __tablename__ = 'posts'
    # Define the columns
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='NOW()')


class User(Base):
    __tablename__ = 'users'
    email = Column(String, nullable = False, unique=True)
    password = Column(String, nullable= False)
    id = Column(Integer, primary_key=True, nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='NOW()')
