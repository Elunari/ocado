import csv
import sys
import pandas as pd
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


def read_csv(filename):
    data = pd.read_csv(filename, header=None)
    return data


def calculate_balances(data):
    balances = defaultdict(int)
    for _, row in data.iterrows():
        creditor, debtor, amount = row
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


if __name__ == "__main__":

    if len(sys.argv) != 3:
        logger.error('Incorrect number of arguments')
        sys.exit(1)

    file_path = sys.argv[1]
    output_path = sys.argv[2]
    csv_data = read_csv(file_path)
    balances = calculate_balances(csv_data)
    payments = calculate_min_payments(balances)
    with open(output_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(payments)
