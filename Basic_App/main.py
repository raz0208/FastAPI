# Import required libraries
from fastapi import FastAPI

# Create main app by calling FastAPI class
app = FastAPI()

# Define a route for the root URL
@app.get("/")
def read_root():
    return {"Hello": "World"}