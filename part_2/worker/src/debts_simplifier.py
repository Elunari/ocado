from collections import defaultdict

def calculate_balances(data):
    
    balances = defaultdict(int)
    
    for row in data:
        creditor, debtor, amount = row
        amount = int(amount)
        balances[creditor] -= amount
        balances[debtor] += amount
    return balances


def calculate_min_payments(balances):

    payments = []

    while any(balances.values()):
        debtor = max(balances, key=balances.get)
        creditor = min(balances, key=balances.get)

        amount = min(abs(balances[debtor]), abs(balances[creditor]))

        payments.append((debtor, creditor, amount))

        balances[creditor] += amount
        balances[debtor] -= amount

    return payments
