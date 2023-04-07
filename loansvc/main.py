from fastapi import FastAPI
from loansvc import db
from loansvc import calc
from loansvc import errors
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

    if loans is None:
        raise errors.NotFoundHTTPException("user", user_id)

    return {'loans': loans}

@app.post("/loan")
def create_loan(loan: models.Loan):
    loan_id = db.create_loan(loan)
    return {'id': loan_id}

@app.get("/loan/{loan_id}")
def get_loan(loan_id: int):
    loan = db.get_loan(loan_id)

    if loan is None:
        raise errors.NotFoundHTTPException("loan", loan_id)

    return {'loan': loan}

@app.get("/loan/{loan_id}/schedule")
def get_loan_schedule(loan_id: int):
    loan = db.get_loan(loan_id)

    if loan is None:
        raise errors.NotFoundHTTPException("loan", loan_id)

    schedule = calc.make_schedule_simple(calc.generate_schedule(loan))

    return {'schedule': schedule}

# TODO: Make this kv param instead
@app.get("/loan/{loan_id}/summary/{month}")
def get_loan_summary(loan_id: int, month: int):
    loan = db.get_loan(loan_id)

    if loan is None:
        raise errors.NotFoundHTTPException("loan", loan_id)

    schedule = calc.generate_schedule(loan)
    summary = calc.generate_summary(schedule, month)

    return {'summary': summary}

@app.put("/loan/{loan_id}/users")
def add_user_to_loan(loan_id: int, user_list: UserList):
    if not db.add_loan_users(loan_id, user_list.user_ids):
        raise errors.NotFoundHTTPException("loan", loan_id)

    return {}