from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error

app = FastAPI() # create an instance of the FastAPI class to define the API application

# MySQL connection function
def get_db_connection():
    db_conecction = mysql.connector.connect(    
        host = "sql7.freesqldatabase.com",
        user = "sql7828943",
        password = "dDgzfCqWSc",
        database = "sql7828943"
    )
    return db_conecction

# test db connection with user fetch
@app.get("/users/") # define a GET endpoint at the path "/users/" to fetch all users from the database
def get_users():
    try:
        connect_to_db = get_db_connection() # establish connection to the database
        cursor = connect_to_db.cursor(dictionary=True) # create a cursor to execute SQL queries, set dictionary=True for better readability
        cursor.execute("SELECT * FROM users") # execute SQL query to fetch all users from the 'users' table
        user_table_rows = cursor.fetchall() # fetch all rows returned by the query and store them in a variable
        cursor.close() # close the cursor after fetching data
        connect_to_db.close() # close the database connection
        return {"users": user_table_rows}
    except mysql.connector.Error as e:
        # return error if connection or query fails
        raise HTTPException(status_code=500, detail=str(e)) # Code 500: if there is an issue with the database connection or query execution