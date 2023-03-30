from fastapi import FastAPI
from pydantic import BaseModel

import sqlite3

app = FastAPI()

# Set up SQLite database connection
# Need to run with 'check_same_thread' since SQLite is file-based
# isn't intended for "multithreaded" apps like a server
conn = sqlite3.connect('/app/mydatabase.db', check_same_thread=False)
print('Database connection established.')

@app.get("/")
def index():
    return {"message": "Welcome to my REST API!"}

class CreateUserPayload(BaseModel):
    name: str

class User(BaseModel):
    id: int
    name: str

# TODO: Put this in a new file
@app.get("/users")
def get_users():
    cursor = conn.execute('SELECT * FROM users;')
    users = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
    return {'users': users}

@app.post("/user")
def create_user(create_request: CreateUserPayload):
    d = create_request.dict()

    # TODO: Implement
    return d