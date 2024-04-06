import unittest
from parameterized import parameterized
import pandas as pd
from main import read_csv, calculate_balances, calculate_min_payments

debts_1 = pd.DataFrame([
    ["Logan", "Jessica", 574], 
    ["Logan", "Mary", 45], 
    ["Logan", "Jessica", 177], 
    ["James", "Jessica", 42], 
    ["Jessica", "James", 169], 
    ["Mary", "James", 651], 
    ["James", "Logan", 461], 
    ["James", "Amanda", 493], 
    ["Mary", "Amanda", 359], 
    ["Jessica", "Amanda", 400], 
    ["Amanda", "James", 439], 
    ["Logan", "Amanda", 605],
    ["James", "Jessica", 232], 
    ["James", "Logan", 742], 
    ["Logan", "Mary", 599], 
    ["Mary", "Logan", 827], 
    ["Logan", "Amanda", 13], 
    ["James", "Jessica", 538], 
    ["James", "Logan", 397], 
    ["Jessica", "James", 952]
])


class TestMain(unittest.TestCase):

    def test_read_csv(self):
        test_csv = '../test_data/debts_1.csv'
        data = read_csv(test_csv)
        self.assertTrue(data.equals(debts_1))

    @parameterized.expand([
        (pd.DataFrame([
            ['Alice', 'Bob', 100],
            ['Bob', 'Charlie', 50],
            ['Alice', 'Charlie', 25]
        ]), {'Alice': -125, 'Bob': 50, 'Charlie': 75}),
        (pd.DataFrame([
            ['Dave', 'Eve', 100],
            ['Eve', 'Dave', 100]
        ]), {'Dave': 0, 'Eve': 0}),
    ])
    def test_calculate_balances(self, data, expected_balances):
        balances = calculate_balances(data)
        self.assertEqual(balances, expected_balances)

    @parameterized.expand([
        ({'Alice': -100, 'Bob': 50, 'Charlie': 50}, [('Charlie', 'Alice', 50), ('Bob', 'Alice', 50)]),
        ({'Dave': 0, 'Eve': 0}, []),
        ({'Fred': -75, 'Gina': -25, 'Harry': 100}, [('Harry', 'Fred', 75), ('Harry', 'Gina', 25)]),
    ])
    def test_calculate_min_payments(self, balances, expected_payments):
        payments = calculate_min_payments(balances)
        self.assertEqual(set(payments), set(expected_payments))  

if __name__ == '__main__':
    unittest.main()