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


############################################################################
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


############################################################################
# ## **Day three of FastAPI Practice**
# #### Handle request and response body using Pydantic models
# from fastapi import FastAPI
# from pydantic import BaseModel, Field, field_validator

# app = FastAPI()

# # # Define a Pydantic model format for item
# # class User(BaseModel):
# #     name: str
# #     age: int

# # # # Define a route to create a user
# # # @app.post("/users/")
# # # async def create_user(user: User):
# # #     return {"sended user": user.name, "sended age": user.age}

# # # Define a route to create a user for response body
# # @app.post("/users/{user_id}", response_model=User)
# # async def create_user(user_id: int):
# #     # Example user data, in a real application you would typically save this to a database
# #     return User(name="John Doe", age=30)

# # Define a Pytdantic model with auto validation
# class User(BaseModel):
#     name: str
#     age: int = Field(..., gt = 0, le = 120, description = "Age must be between 1 and 120")

#     @field_validator("name")
#     def name_must_not_be_empty(cls, value):
#         if not value:
#             raise ValueError("Name must not be empty")
#         return value

# @app.post("/users/")
# async def create_user(user: User):
#     # Example user data, in a real application you would typically save this to a database
#     user_data = {"name": user.name, "age": user.age}
#     return user_data

############################################################################

## **Day four of FastAPI Practice: Pydantic Models**
### Example Usage: Validation user data for registration form

# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# class User(BaseModel):
#     username: str
#     email: str
#     age: int

# @app.post("/register/")

# async def register_user(user: User):
#     # In a real application, you would typically save this to a database
#     return user

# Use advanced validation with Pydantic and regular expressions
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, field_validator
"""
EmailStr: Validates that the input is a valid email address.
conint: Validates that the input is an integer and can enforce constraints.
constr: Validates that the input is a string and can enforce constraints.
"""

app = FastAPI()

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$')
    email: EmailStr
    age: int = Field(..., gt=0, le=120)

    # You can also add custom validation logic using validators
    @field_validator("username")
    def username_must_not_contain_spaces(cls, value):
        if " " in value:
            raise ValueError("Username must not contain spaces.")
        return value
        
@app.post("/register/")
async def register_user(user: User):
    # In a real application, you would typically save this to a database
    return user