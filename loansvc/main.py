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

@app.get("/user/{user_id}/loans")
def get_user_loans(user_id: int):
    loans = db.get_user_loans(user_id)
    return {'loans': loans}

@app.post("/loan/{user_id}")
def create_loan_for_user(user_id: int, loan: models.Loan):
    loan_id = db.create_loan_for_user(loan, user_id)
    return {'id': loan_id}