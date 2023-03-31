from loansvc import models
from sqlmodel import Session, create_engine, select
from typing import List

DB_URI = "sqlite:////app/mydatabase.db"

def get_all_users() -> List[models.User]:
    engine = create_engine(DB_URI)
    with Session(engine) as session:
        return session.exec(select(models.User)).all()

def get_user_loans(user_id: int) -> models.User:
    engine = create_engine(DB_URI)
    with Session(engine) as session:
        # TODO: Need error handling here
        return session.exec(select(models.User).where(models.User.id == user_id)).first().loans

def create_user(user: models.User) -> int:
    engine = create_engine(DB_URI)
    with Session(engine) as session:
        session.add(user)
        session.commit()

        return user.id

def create_loan_for_user(loan: models.Loan, user_id: int):
    engine = create_engine(DB_URI)
    with Session(engine) as session:
        user = session.get(models.User, user_id)
        loan.users = [user]
        session.add(loan)
        session.commit()

        return loan.id