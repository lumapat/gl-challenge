from fastapi import FastAPI
from loansvc import db
from loansvc import models
from pydantic import BaseModel
from typing import List

app = FastAPI()

class UserList(BaseModel):
    user_ids: List[int]

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

@app.get("/user/{user_id}/loans")
def get_user_loans(user_id: int):
    loans = db.get_user_loans(user_id)
    return {'loans': loans}

@app.post("/loan")
def create_loan(loan: models.Loan):
    loan_id = db.create_loan(loan)
    return {'id': loan_id}

@app.get("/loan/{loan_id}")
def get_loan(loan_id: int):
    loan = db.get_loan(loan_id)
    return {'loan': loan}

@app.put("/loan/{loan_id}/users")
def add_user_to_loan(loan_id: int, user_list: UserList):
    db.add_loan_users(loan_id, user_list.user_ids)
    return {}