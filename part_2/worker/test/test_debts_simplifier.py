import pytest
from src.debts_simplifier import calculate_balances, calculate_min_payments


@pytest.mark.parametrize(
    "data,expected_balances",
    [
        (
            [["Alice", "Bob", 100], ["Bob", "Charlie", 50], ["Alice", "Charlie", 25]],
            {"Alice": -125, "Bob": 50, "Charlie": 75},
        ),
        ([["Dave", "Eve", 100], ["Eve", "Dave", 100]], {"Dave": 0, "Eve": 0}),
    ],
)
def test_calculate_balances(data, expected_balances):
    balances = calculate_balances(data)
    assert balances == expected_balances


@pytest.mark.parametrize(
    "balances,expected_payments",
    [
        (
            {"Alice": -100, "Bob": 50, "Charlie": 50},
            [("Charlie", "Alice", 50), ("Bob", "Alice", 50)],
        ),
        ({"Dave": 0, "Eve": 0}, []),
        (
            {"Fred": -75, "Gina": -25, "Harry": 100},
            [("Harry", "Fred", 75), ("Harry", "Gina", 25)],
        ),
    ],
)
def test_calculate_min_payments(balances, expected_payments):
    payments = calculate_min_payments(balances)
    assert set(payments) == set(expected_payments)
