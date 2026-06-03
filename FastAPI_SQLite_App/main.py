# Import SQLalchemy libraries
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# Import FastAPI required libraries
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

# Create an instance of the FastAPI class to define the API application
app = FastAPI()

# Define the database URL for SQLite
DATABASE_URL = "sqlite:///./test.db" # SQLite database file will be created in the current directory with the name 'test.db'

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # connect_args is required for SQLite to allow multiple threads to access the database

# Create a sessionmaker factory to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models using the declarative system
Base = declarative_base() # Foundation for all our database models

# Define a User model that represents the users table in the database
class User(Base):
    __tablename__ = "users" # Name of the table in the database

    id = Column(Integer, primary_key = True, index = True) # Primary key column for the user ID
    name = Column(String, index = True) # Column for the user's name
    email = Column(String, index = True, unique = True) # Column for the user's email, which must be unique
    age = Column(Integer) # Column for the user's age

# Create the actual database tables based on the defined models
Base.metadata.create_all(bind = engine) # This will create the 'users' table in the SQLite database if it doesn't already exist

# Define function to dependency to get a database session
def get_db():
    db = SessionLocal() # Create a new database session
    try:
        yield db # Yield the session to be used in API endpoints
    finally:
        db.close() # Ensure the database session is closed after use

# Define a Pydantic model for handle input data
class UserCreate(BaseModel):
    id: int
    name: str
    email: str
    age: int

    class Config:
        orm_mode = True # This allows the Pydantic model to work with SQLAlchemy models

# Create Operation: Define API endpoint to create a new user
@app.post("/users/", response_model = UserCreate) # This endpoint will accept POST requests to create a new user and return the created user as a response
def create_user(user: UserCreate, db: Session = Depends(get_db)): # The function takes a userCreate object as input and a database session as a dependency
    db_user = User(name = user.name, email = user.email, age = user.age) # Create a new User instance with the provided data
    db.add(db_user) # Add the new user to the database session
    db.commit() # Save the changes in the database
    db.refresh(db_user) # Refresh the instance to get the updated data from the database
    return db_user # Return the created user as a response

# Read Operation: Define API endpoint to retrieve data from databse
@app.get("/users/", response_model = List[UserCreate]) # This endpoint will accept GET requests to retrieve all users and return a list of users as a response
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)): # The function takes optional query parameters for pagination and a database session as a dependency
    users = db.query(User).offset(skip).limit(limit).all() # Query the database to get a list of users with pagination
    return users # Return the list of users as a response

# Read Operation: Define API endpoint to retrieve a specific user by ID
@app.get("/users/{user_id}", response_model = UserCreate) # This endpoint will accept
def read_user(user_id: int, db: Session = Depends(get_db)): # The function takes a user ID as a path parameter and a database session as a dependency
    user = db.query(User).filter(User.id == user_id).first() # Query the database to get the user with the specified ID
    if user is None: # If no user is found, raise an HTTP 404 error
        raise HTTPException(status_code = 404, detail = "User not found")
    return user # Return the found user as a response

# Create pydantic model for updating user data
class UserUpdate(BaseModel):
    name: Optional[str] = None # Optional field for the user's name
    email: Optional[str] = None # Optional field for the user's email
    age: Optional[int] = None # Optional field for the user's age

# Update Operation: Define FastAPI endpoint to modify an existing user
@app.put("/users/{user_id}", response_model = UserUpdate) # This endpoint will accept PUT requests to update an existing user
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)): # The function takes a user ID as a path parameter, a UserUpdate object as input, and a database session as a dependency
    db_user = db.query(User).filter(User.id == user_id).first() # Query the database to get the user with the specified ID

    if db_user is None: # If no user is found, raise an HTTP 404 error
        raise HTTPException(status_code = 404, detail = "User not found")
    
    db_user.name = user.name if user.name is not None else db_user.name # Update the user's name if provided, otherwise keep the existing name
    db_user.email = user.email if user.email is not None else db_user.email # Update the user's email if provided, otherwise keep the existing email
    db_user.age = user.age if user.age is not None else db_user.age # Update the user's age if provided, otherwise keep the existing age
    db.commit() # Save the changes in the database
    db.refresh(db_user) # Refresh the instance to get the updated data from the database
    return db_user # Return the updated user as a response

# Delete Operation: Using FastAPI endpoint to remove a user from the database
@app.delete ("/users/{user_id}", response_model = UserCreate) # This endpoint will accept DELETE requests to remove a user from the database
def delete_user(user_id: int, db: Session = Depends(get_db)): # The function takes a user ID as a path parameter and a database session as a dependency
    db_user = db.query(User).filter(User.id == user_id).first() # Query the database to get the user with the specified ID

    if db_user is None: # If no user is found, raise an HTTP 404 error
        raise HTTPException(status_code = 404, detail = "User not found")
    
    db.delete(db_user) # Delete the user from the database session
    db.commit() # Save the changes in the database
    return db_user # Return the deleted user as a response