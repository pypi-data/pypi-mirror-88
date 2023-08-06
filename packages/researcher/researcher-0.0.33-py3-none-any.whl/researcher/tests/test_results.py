import unittest

import researcher as rs

TEST_DATA_PATH = "data/"

class TestResults(unittest.TestCase):
    def setUp(self):
        self.e1 = rs.load_experiment(TEST_DATA_PATH, "example_record.json")
        self.e2 = rs.load_experiment(TEST_DATA_PATH, "example_epoch_record.json")
    
    def test_correctly_gathers_metric(self):
        mses = self.e1.get_metric("mse")   

        self.assertEqual(len(mses), 5)
        self.assertEqual(len(mses[0]), 1)
        self.assertEqual(len(mses[1]), 1)
        self.assertEqual(len(mses[2]), 1)
        self.assertEqual(len(mses[3]), 1)
        self.assertEqual(len(mses[4]), 1)

        mses = self.e2.get_metric("mse")   

        self.assertEqual(len(mses), 5)
        self.assertEqual(len(mses[0]), 2)
        self.assertEqual(len(mses[1]), 2)
        self.assertEqual(len(mses[2]), 2)
        self.assertEqual(len(mses[3]), 2)
        self.assertEqual(len(mses[4]), 2)
