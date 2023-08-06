import unittest

import researcher as rs

from tests.tools import TEST_DATA_PATH

class TestObservationAnalysis(unittest.TestCase):
    def setUp(self):
        self.e1 = rs.load_experiment(TEST_DATA_PATH, "example_record_28hbsb12bns8612vt26867156.json")
        self.e2 = rs.load_experiment(TEST_DATA_PATH, "example_epoch_record_sadasd328234g123v213b31271bn.json")
        self.e3 = rs.load_experiment(TEST_DATA_PATH, "example_record_general_8231213hj9812nba8hnsd.json")
    
    def test_correctly_loads_general_observations(self):
        self.assertAlmostEqual(self.e3.observations["flange_loss"], 0.44)

    def test_correctly_returns_fold_metrics(self):
        self.assertEqual(self.e2.observations["mse"], [[0.45,0.78], [0.89,0.11], [0.33,0.21], [0.22, 0.09], [1.03, 0.72]])
        self.assertEqual(self.e2.final_observations("mse"), [0.78, 0.11, 0.21, 0.09, 0.72])

    def test_correctly_gathers_metric(self):
        mses = self.e1.observations["mse"]   

        self.assertEqual(len(mses), 5)
        self.assertEqual(len(mses[0]), 1)
        self.assertEqual(len(mses[1]), 1)
        self.assertEqual(len(mses[2]), 1)
        self.assertEqual(len(mses[3]), 1)
        self.assertEqual(len(mses[4]), 1)

        mses = self.e2.observations["mse"]   

        self.assertEqual(len(mses), 5)
        self.assertEqual(len(mses[0]), 2)
        self.assertEqual(len(mses[1]), 2)
        self.assertEqual(len(mses[2]), 2)
        self.assertEqual(len(mses[3]), 2)
        self.assertEqual(len(mses[4]), 2)

    def test_saves_multiple_fold_observations(self):
        rb = rs.ObservationCollector()
        rb.add_fold_observations(0, "loss", [0.5, 0.5, 0.5, 0.5])

        self.assertEqual(rb.observations["loss"], [[0.5, 0.5, 0.5, 0.5]])

        rb.add_fold_observations(1, "loss", [0.5, 0.44, 0.43, 0.4])
        self.assertEqual(rb.observations["loss"], [[0.5, 0.5, 0.5, 0.5],  [0.5, 0.44, 0.43, 0.4]])

    def test_prevents_fold_metrics_with_general_metric_names(self):
        rb = rs.ObservationCollector()
        rb.set_observation("loss", 0.5)

        self.assertRaises(ValueError, rb.add_fold_observation, 0, "loss", 0.5)
        self.assertRaises(ValueError, rb.add_fold_observation, 0, "loss", 0.2)
        self.assertRaises(ValueError, rb.add_fold_observation, 0, "loss", 0.1)

        rb.add_fold_observation(0, "fold_loss", 0.5)

    def test_prevents_general_metrics_with_fold_metric_names(self):
        rb = rs.ObservationCollector()

        rb.add_fold_observation(0, "loss", 0.5)
        rb.add_fold_observation(0, "loss", 0.2)
        rb.add_fold_observation(0, "loss", 0.1)

        self.assertRaises(ValueError, rb.set_observation, "loss", 0.5)
        self.assertRaises(ValueError, rb.set_observation, "loss", 0.2)
        self.assertRaises(ValueError, rb.set_observation, "loss", 0.1)

        rb.set_observation("general_loss", 0.5)

    def test_prevents_general_metrics_with_fold_metric_names_multiple(self):
        rb = rs.ObservationCollector()

        rb.add_fold_observations(0, "loss", [0.5, 0.5, 0.5, 0.5])
        rb.add_fold_observations(0, "loss", [0.2, 0.2, 0.2, 0.2])
        rb.add_fold_observations(0, "loss", [0.1, 0.1, 0.1, 0.1])

        self.assertRaises(ValueError, rb.set_observation, "loss", 0.5)
        self.assertRaises(ValueError, rb.set_observation, "loss", 0.2)
        self.assertRaises(ValueError, rb.set_observation, "loss", 0.1)

        rb.set_observation("general_loss", [0.5, 4.7, 5.0])

    def test_prevents_general_metrics_being_overwritten(self):
        rb = rs.ObservationCollector()
        rb.set_observation("loss", 0.5)
        self.assertRaises(ValueError, rb.set_observation, "loss", 0.5)
        self.assertRaises(ValueError, rb.set_observation, "loss", 0.2)
        self.assertRaises(ValueError, rb.set_observation, "loss", 0.1)

    def test_collects_dictionary(self):
        rb = rs.ObservationCollector()
        rb.set_observations({
            "loss": 0.6,
            "f-loss": 0.98,
            "score": [5, 6, 7],
            "flange-error": [[0.55, 0.66], [0.87, 0.78]]
        })

        self.assertAlmostEqual(rb.observations["loss"], 0.6, 7)
        self.assertEqual(rb.observations["flange-error"],[[0.55, 0.66], [0.87, 0.78]])

        self.assertRaises(ValueError, rb.add_fold_observation, 0, "loss", 0.4)
        self.assertRaises(ValueError, rb.add_fold_observation, 1, "loss", 0.4)
        self.assertRaises(ValueError, rb.add_fold_observation, 0, "flange-error", 0.4)

        rb.add_fold_observation(0, "new-metric", 0.4)


    
