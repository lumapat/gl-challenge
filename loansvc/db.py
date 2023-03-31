from loansvc.models import User
from sqlmodel import Session, create_engine, select
from typing import List

DB_URI = "sqlite:////app/mydatabase.db"

def get_all_users() -> List[User]:
    engine = create_engine(DB_URI)
    with Session(engine) as session:
        return session.exec(select(User)).all()

def create_user(user: User) -> int:
    engine = create_engine(DB_URI)
    with Session(engine) as session:
        session.add(user)
        session.commit()

        return user.id