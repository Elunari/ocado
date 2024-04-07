import unittest
import csv
import os
from main import main

class TestMainIntegration(unittest.TestCase):
    def test_app_output(self):
        input_csv_path = '../test_data/debts_1.csv'
        output_csv_path = '../test_data/results.csv'
        expected_output_csv_path = '../test_data/results_1.csv'
        
        main(input_csv_path, output_csv_path)

        with open(output_csv_path, newline='') as actual_file:
            actual_reader = csv.reader(actual_file)
            actual_data = list(actual_reader)
        
        with open(expected_output_csv_path, newline='') as expected_file:
            expected_reader = csv.reader(expected_file)
            expected_data = list(expected_reader)

        self.assertEqual(actual_data, expected_data)
        os.remove(output_csv_path)

if __name__ == '__main__':
    unittest.main()