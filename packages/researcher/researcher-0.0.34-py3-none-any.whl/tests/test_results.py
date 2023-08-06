import unittest

import researcher as rs

from tests.tools import TEST_DATA_PATH

class TestResultAnalysis(unittest.TestCase):
    def setUp(self):
        self.e1 = rs.load_experiment(TEST_DATA_PATH, "example_record.json")
        self.e2 = rs.load_experiment(TEST_DATA_PATH, "example_epoch_record.json")
        self.e3 = rs.load_experiment(TEST_DATA_PATH, "example_record_general.json")
    
    def test_correctly_loads_general_results(self):
        self.assertAlmostEqual(self.e3.general_results["flange_loss"], 0.44)

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

    def test_prevents_fold_metrics_with_general_metric_names(self):
        rb = rs.ResultBuilder()
        rb.set_general_metric("loss", 0.5)

        self.assertRaises(ValueError, rb.add, 0, "loss", 0.5)
        self.assertRaises(ValueError, rb.add, 0, "loss", 0.2)
        self.assertRaises(ValueError, rb.add, 0, "loss", 0.1)

        rb.add(0, "fold_loss", 0.5)

    def test_prevents_general_metrics_with_fold_metric_names(self):
        rb = rs.ResultBuilder()

        rb.add(0, "loss", 0.5)
        rb.add(0, "loss", 0.2)
        rb.add(0, "loss", 0.1)

        self.assertRaises(ValueError, rb.set_general_metric, "loss", 0.5)
        self.assertRaises(ValueError, rb.set_general_metric, "loss", 0.2)
        self.assertRaises(ValueError, rb.set_general_metric, "loss", 0.1)

        rb.set_general_metric("general_loss", 0.5)

    def test_prevents_general_metrics_being_overwritten(self):
        rb = rs.ResultBuilder()
        rb.set_general_metric("loss", 0.5)
        self.assertRaises(ValueError, rb.set_general_metric, "loss", 0.5)
        self.assertRaises(ValueError, rb.set_general_metric, "loss", 0.2)
        self.assertRaises(ValueError, rb.set_general_metric, "loss", 0.1)



    
