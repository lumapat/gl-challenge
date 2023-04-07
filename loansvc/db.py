from loansvc import models
from sqlmodel import Session, create_engine, select
from typing import List, Optional

DB_URI = "sqlite:////app/mydatabase.db"

def get_all_users() -> List[models.User]:
    engine = create_engine(DB_URI)
    with Session(engine) as session:
        return session.exec(select(models.User)).all()

def get_user_loans(user_id: int) -> Optional[models.User]:
    engine = create_engine(DB_URI)
    with Session(engine) as session:
        # TODO: Possible we can return multiple users (from some DB mishap)
        #       but currently not possible from PK invariant
        user = session.exec(select(models.User).where(models.User.id == user_id)).first()

        if not user:
            return None

        return user.loans

def create_user(user: models.User) -> int:
    engine = create_engine(DB_URI)
    with Session(engine) as session:
        session.add(user)
        session.commit()

        return user.id

def create_loan_for_user(loan: models.Loan, user_id: int) -> int:
    engine = create_engine(DB_URI)
    with Session(engine) as session:
        user = session.get(models.User, user_id)
        loan.users = [user]
        session.add(loan)
        session.commit()

        return loan.id

def create_loan(loan: models.Loan) -> int:
    engine = create_engine(DB_URI)
    with Session(engine) as session:
        session.add(loan)
        session.commit()

        return loan.id

def get_loan(loan_id: int) -> Optional[models.Loan]:
    engine = create_engine(DB_URI)
    with Session(engine) as session:
        return session.get(models.Loan, loan_id)


def add_loan_users(loan_id: int, user_ids: List[int]) -> bool:
    engine = create_engine(DB_URI)
    with Session(engine) as session:
        loan = session.get(models.Loan, loan_id)

        if not loan:
            return False

        user_id_clauses = [
            models.User.id == user_id
            for user_id in user_ids
        ]

        user_query = select(models.User).where(*user_id_clauses)
        users = session.exec(user_query)
        loan.users.extend(users)

        session.add(loan)
        session.commit()

        return True