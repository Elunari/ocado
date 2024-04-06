import csv
import sys
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


def read_csv(file_path):
    
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data


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

def main(input_path, output_path):
    csv_data = read_csv(input_path)
    balances = calculate_balances(csv_data)
    payments = calculate_min_payments(balances)
    with open(output_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(payments)

if __name__ == "__main__":

    if len(sys.argv) != 3:
        logger.error('Incorrect number of arguments')
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
