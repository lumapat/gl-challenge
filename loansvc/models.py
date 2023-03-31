from decimal import Decimal
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional

class LoanUser(SQLModel, table=True):
    __tablename__ = "loan_user"
    user_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="user.id")
    loan_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="loan.id")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    loans: List["Loan"] = Relationship(back_populates="users", link_model=LoanUser)

class Loan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    loan_term: int
    amount: Decimal
    annual_ir: Decimal
    users: List[User] = Relationship(back_populates="loans", link_model=LoanUser)
