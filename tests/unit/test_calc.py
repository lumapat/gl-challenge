from loansvc.calc import generate_schedule, generate_summary, make_schedule_simple, SimpleLoanScheduleEntry, LoanScheduleEntry
from loansvc.models import Loan
from decimal import Decimal

def compare_schedule_entry(expected: SimpleLoanScheduleEntry, actual: SimpleLoanScheduleEntry):
    epsilon = 1e-2
    assert expected.month == actual.month
    assert abs(expected.remaining_balance - actual.remaining_balance) < epsilon
    assert abs(expected.monthly_payment - actual.monthly_payment) < epsilon


def test_generate_schedule():
    # GIVEN
    loan = Loan(
        loan_term=6,
        amount=Decimal(2000),
        annual_ir=Decimal(6)
    )

    # WHEN
    schedule = make_schedule_simple(generate_schedule(loan))

    # THEN
    expected_schedule = [
        SimpleLoanScheduleEntry(month=1, remaining_balance=Decimal('1903.76'), monthly_payment=Decimal('96.24')),
        SimpleLoanScheduleEntry(month=2, remaining_balance=Decimal('1759.40'), monthly_payment=Decimal('144.36')),
        SimpleLoanScheduleEntry(month=3, remaining_balance=Decimal('1542.86'), monthly_payment=Decimal('216.54')),
        SimpleLoanScheduleEntry(month=4, remaining_balance=Decimal('1218.05'), monthly_payment=Decimal('324.81')),
        SimpleLoanScheduleEntry(month=5, remaining_balance=Decimal('730.83'), monthly_payment=Decimal('487.22')),
        SimpleLoanScheduleEntry(month=6, remaining_balance=Decimal('0'), monthly_payment=Decimal('730.83')),
    ]

    assert len(expected_schedule) == len(schedule)
    for e,a in zip(expected_schedule, schedule):
        compare_schedule_entry(e, a)


def test_generate_schedule_really_short_term():
    # GIVEN
    loan = Loan(
        loan_term=1,
        amount=Decimal(2000),
        annual_ir=Decimal(5)
    )

    # WHEN
    schedule = make_schedule_simple(generate_schedule(loan))

    # THEN
    expected_schedule = [
        SimpleLoanScheduleEntry(month=1, remaining_balance=Decimal('0'), monthly_payment=loan.amount)
    ]

    assert len(expected_schedule) == len(schedule)
    for e,a in zip(expected_schedule, schedule):
        compare_schedule_entry(e, a)


def test_generate_schedule_no_interest():
    # GIVEN
    loan = Loan(
        loan_term=12,
        amount=Decimal(2400),
        annual_ir=Decimal(0)
    )

    # WHEN
    schedule = make_schedule_simple(generate_schedule(loan))

    # THEN
    monthly_payment = loan.amount / loan.loan_term
    expected_schedule = [
        SimpleLoanScheduleEntry(
            month=m,
            remaining_balance=loan.amount - Decimal(m) * monthly_payment,
            monthly_payment=monthly_payment)
        for m in range(1, loan.loan_term+1)
    ]

    assert len(expected_schedule) == len(schedule)
    for e,a in zip(expected_schedule, schedule):
        compare_schedule_entry(e, a)


def test_generate_schedule_no_loan_term():
    # GIVEN
    loan = Loan(
        loan_term=0,
        amount=Decimal(1000),
        annual_ir=Decimal(6)
    )

    # WHEN
    schedule = make_schedule_simple(generate_schedule(loan))

    # THEN
    assert schedule == []


def test_generate_schedule_no_amount():
    # GIVEN
    loan = Loan(
        loan_term=24,
        amount=Decimal(0),
        annual_ir=Decimal(6)
    )

    # WHEN
    schedule = make_schedule_simple(generate_schedule(loan))

    # THEN
    assert schedule == []


def test_generate_summary():
    # GIVEN
    term = 6
    balance = 3600
    monthly_payment = 600
    schedule = [
        LoanScheduleEntry(
            month=i,
            remaining_balance=balance - i * monthly_payment,
            raw_monthly_payment=monthly_payment,
            adjusted_monthly_payment=monthly_payment,
            interest_accrued=70 - i * 10,
        )
        for i in range(1, term+1)
    ]

    # WHEN
    summary = generate_summary(schedule, 4)

    # THEN
    assert summary.month == 4
    assert summary.current_principal_balance == 1200
    assert summary.aggregate_interest_paid == 180
    assert summary.aggregate_principal_paid == 2400


def test_generate_summary_bad_month():
    # GIVEN
    schedule = [
        LoanScheduleEntry(
            month=1,
            remaining_balance=0,
            raw_monthly_payment=2400,
            adjusted_monthly_payment=2400,
            interest_accrued=0,
        )
    ]

    # WHEN
    try:
        _ = generate_summary(schedule, 0)
        assert False, "expecting exception"
    except:
        assert True
