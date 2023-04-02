from dataclasses import dataclass
from decimal import Decimal
from loansvc.models import Loan
from typing import List


@dataclass
class SimpleLoanScheduleEntry:
    month: int
    remaining_balance: Decimal
    monthly_payment: Decimal

@dataclass
class LoanScheduleEntry:
    month: int
    remaining_balance: Decimal
    raw_monthly_payment: Decimal
    adjusted_monthly_payment: Decimal
    interest_accrued: Decimal

@dataclass
class LoanSummary:
    month: int
    current_principal_balance: Decimal
    aggregate_principal_paid: Decimal
    aggregate_interest_paid: Decimal


# TODO: We might want to associate the loan's ID here
LoanSchedule = List[LoanScheduleEntry]
SimpleLoanSchedule = List[SimpleLoanScheduleEntry]

def make_schedule_simple(schedule: LoanSchedule) -> SimpleLoanSchedule:
    return [
        SimpleLoanScheduleEntry(
            month=e.month,
            remaining_balance=e.remaining_balance,
            monthly_payment=e.adjusted_monthly_payment,
        )
        for e in schedule
    ]

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
            raw_monthly_payment=monthly_payment,
            adjusted_monthly_payment=adjusted_payment,
            interest_accrued=interest,
        ))

    return schedule


def generate_summary(schedule: LoanSchedule, month: int) -> LoanSummary:
    pass