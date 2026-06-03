# Import SQLalchemy libraries
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# Import FastAPI required libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create an instance of the FastAPI class to define the API application
app = FastAPI()

# Define the database URL for SQLite
DATABASE_URL = "sqlite:///./test.db" # SQLite database file will be created in the current directory with the name 'test.db'

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # connect_args is required for SQLite to allow multiple threads to access the database

# Create a sessionmaker factory to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models using the declarative system
Base = declarative_base(): # Foundation for all our database models

# Define a User model that represents the users table in the database
class User(Base):
    __tablename__ = "users" # Name of the table in the database

    id = Column(Integer, primary_key = True, index = true, limit = 10) # Primary key column for the user ID
    name = Column(String, index = True) # Column for the user's name
    email = Column(String, Unique = True, index = True) # Column for the user's email, which must be unique
    age = Column(Integer, limit = from 0 to 120, nullable = True) # Column for the user's age, with a limit of 0 to 120

# Create the actual database tables based on the defined models
Base.metadata.create_all(bind = engine) # This will create the 'users' table in the SQLite database if it doesn't already exist

# Define function to dependency to get a database session
def get_db():
    db = SessionLocal() # Create a new database session
    try:
        yield db # Yield the session to be used in API endpoints
    finally:
        db.close() # Ensure the database session is closed after use

# Define API endpoint to create a new user
@app.post("/users/", response_model = User) # This endpoint will accept POST requests to create a new user and return the created user as a response
def create_user(user: User, db: Session = Depends(get_db))