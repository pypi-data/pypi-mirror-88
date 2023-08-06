import unittest
import os
import glob

import researcher as rs
import numpy as np

from tests.tools import TEST_EXPERIMENT_PATH

class TestSavingExperiment(unittest.TestCase):  
    def setUp(self):
        files = glob.glob(TEST_EXPERIMENT_PATH + "*")
        for f in files:
            os.remove(f)

    def test_records_correctly(self):
        params = {
            "title": "cool_experiment",
            "learning_rate": 0.003,
            "batch_size": 32,
            "alpha": 2e-9,
            "model": "rnn",
        }

        res = rs.ObservationCollector()

        for i in range(3):
            for j in range(1, 8):
                res.add_fold_observation(i, "rmse", 0.98 / j)

        rs.record_experiment_with_collector(params, TEST_EXPERIMENT_PATH, res)

        self.assertTrue(os.path.isfile(TEST_EXPERIMENT_PATH + "cool_experiment_d45dee5991986a5b8215706f5e904b3e.json"))

    def test_records_correctly_if_given_dict(self):
        params = {
            "title": "cool_experiment",
            "learning_rate": 0.003,
            "batch_size": 32,
            "alpha": 2e-9,
            "model": "rnn",
        }

        res = rs.ObservationCollector()

        for i in range(3):
            for j in range(1, 8):
                res.add_fold_observation(i, "rmse", 0.98 / j)

        rs.record_experiment(params, TEST_EXPERIMENT_PATH, observations=res.observations)

        self.assertTrue(os.path.isfile(TEST_EXPERIMENT_PATH + "cool_experiment_d45dee5991986a5b8215706f5e904b3e.json"))
    
    def test_records_numpy_integers(self):
        params = {
            "title": "cool_experiment",
            "learning_rate": 0.003,
            "batch_size": np.int64(32),
            "alpha": 2e-9,
            "model": "rnn",
        }

        rs.record_experiment(params, TEST_EXPERIMENT_PATH, observations=None)
        self.assertTrue(os.path.isfile(TEST_EXPERIMENT_PATH + "cool_experiment_d45dee5991986a5b8215706f5e904b3e.json"))

    def test_records_NANs_as_zero(self):
        params = {
            "title": "cool_experiment",
            "learning_rate": 0.003,
            "batch_size": np.int64(32),
            "alpha": 2e-9,
            "model": "rnn",
        }

        res = rs.ObservationCollector()

        for i in range(3):
            for j in range(1, 8):
                res.add_fold_observation(i, "rmse", float('nan'))

        rs.record_experiment(params, TEST_EXPERIMENT_PATH, observations=res.observations)

        self.assertTrue(os.path.isfile(TEST_EXPERIMENT_PATH + "cool_experiment_d45dee5991986a5b8215706f5e904b3e.json"))
        e = rs.load_experiment(TEST_EXPERIMENT_PATH, "cool_experiment_d45dee5991986a5b8215706f5e904b3e.json")