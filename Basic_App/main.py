# Import required libraries
from fastapi import FastAPI

# Create main app by calling FastAPI class
app = FastAPI()

# Define a route for the root URL
@app.get("/")
def read_root():
    return {"Message": "Wlcome to FastAPI!"}

# Define a simple route using post method
@app.post("/items/")
def create_item(name: str, price: float):
    return {"Name": name, "price": price}

# Define a simple route using put method
@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, price: float):
    return {"item_id": item_id, "Name": name, "price": price}

# Define a simple route using delete method
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"item_id": item_id, "Message": "Item deleted successfully!"}