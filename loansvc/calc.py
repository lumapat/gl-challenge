from dataclasses import dataclass
from decimal import Decimal
from loansvc.models import Loan
from typing import List


@dataclass
class LoanScheduleEntry:
    month: int
    remaining_balance: Decimal
    monthly_payment: Decimal

LoanSchedule = List[LoanScheduleEntry]

def generate_schedule(loan: Loan) -> LoanSchedule:
    # Simple validation to not throw off the schedule formula
    if loan.loan_term <= 0 or loan.amount <= 0:
        return []

    # Calculate the monthly payment
    monthly_interest_rate = loan.annual_ir / 12
    num_payments = loan.loan_term

    if loan.annual_ir > 0:
        monthly_payment = (loan.amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate)**(-num_payments))
    else:
        monthly_payment = loan.amount / num_payments # Simple divison in this case

    # Set the starting balance
    balance = loan.amount

    schedule = []
    for i in range(1, num_payments+1):
        # Calculate the ending balance
        interest = balance * monthly_interest_rate
        adjusted_payment = monthly_payment - interest
        balance -= adjusted_payment

        schedule.append(LoanScheduleEntry(
            month=i,
            remaining_balance=balance,
            monthly_payment=adjusted_payment,
        ))

    return schedule