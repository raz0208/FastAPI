## **Day one of FastAPI Practice**

# # Import required libraries
# from fastapi import FastAPI

# # Create main app by calling FastAPI class
# app = FastAPI()

# # Define a route for the root URL
# @app.get("/")
# def read_root():
#     return {"Message": "Wlcome to FastAPI!"}

# # Define a simple route using post method
# @app.post("/items/")
# def create_item(name: str, price: float):
#     return {"Name": name, "price": price}

# # Define a simple route using put method
# @app.put("/items/{item_id}")
# def update_item(item_id: int, name: str, price: float):
#     return {"item_id": item_id, "Name": name, "price": price}

# # Define a simple route using delete method
# @app.delete("/items/{item_id}")
# def delete_item(item_id: int):
#     return {"item_id": item_id, "Message": "Item deleted successfully!"}

# ## **Day two of FastAPI Practice**
# from fastapi import FastAPI

# app = FastAPI()

# # # Define a route for user path parameter
# # @app.get("/users/{user_id}")
# # def read_user(user_id: int):
# #     return {"user_id": user_id}

# # # Define a route for string path parameter
# # @app.get("/items/{item_name}")
# # def read_item(item_name: str):
# #     return {"item_name": item_name}

# # # Define a route for query parameters
# # @app.get("/users/")
# # def road_user(user_id: int, name: str):
# #     return {"user_id": user_id, "name": name}

# @app.get("/users/{user_id}/details")
# def read_user_details(user_id: int, include_email: bool = False):
#     # user_details = {"user_id": user_id, "name": "John Doe"}
#     if include_email:
#         return {"user_id": user_id, "email": "include_email"}
#     else:
#         return {"user_id": user_id, "email": "Email not included"}

## **Day three of FastAPI Practice**
#### Handle request and response body using Pydantic models
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model format for item
class User(BaseModel):
    name: str
    age: int

# # Define a route to create a user
# @app.post("/users/")
# async def create_user(user: User):
#     return {"sended user": user.name, "sended age": user.age}

# Define a route to create a user for response body
@app.post("/users/{user_id}", response_model=User)
async def create_user(user_id: int):
    # Example user data, in a real application you would typically save this to a database
    return User(name="John Doe", age=30)