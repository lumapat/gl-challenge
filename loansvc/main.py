from fastapi import FastAPI
from loansvc import db
from loansvc import models

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Welcome to my REST API!"}

@app.get("/users")
def get_users():
    users = db.get_all_users()
    return {'users': users}

@app.post("/user")
def create_user(user: models.User):
    user_id = db.create_user(user)
    return {'id': user_id}