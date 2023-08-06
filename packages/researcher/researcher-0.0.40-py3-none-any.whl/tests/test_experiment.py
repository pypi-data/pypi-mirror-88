from researcher.experiment import Experiment
import unittest
import json

import numpy as np
import researcher as rs

from tests.tools import TEST_DATA_PATH

class TestExperiment(unittest.TestCase):
    def test_records_observations_correctly(self):
        data = {
            "title": "test",
            "description": "this is the first example record",
            "experiment": "linear_reg",
            "data_name": "data/train.csv",
            "folds": 5,
            "pipeline": "noop",
            "metrics": [
                "mse"
            ],
            "x_cols": [
                "building_id"
            ],
            "y_cols": [
                "meter_reading"
            ],
            "timestamp": "2020-07-11_12:48:55",
            "hash": "28hbsb12bns8612vt26867156",
            "observations": {
                "mse": [
                    [
                        18899806900.366104
                    ],
                    [
                        65922637417.14631
                    ],
                    [
                        29483771984.313713
                    ],
                    [
                        73728779.50177501
                    ],
                    [
                        3029002638.4022694
                    ]
                ]
            }
        }

        expected_observations = {
                "mse": [
                    [
                        18899806900.366104
                    ],
                    [
                        65922637417.14631
                    ],
                    [
                        29483771984.313713
                    ],
                    [
                        73728779.50177501
                    ],
                    [
                        3029002638.4022694
                    ]
                ]
            }

        e = Experiment(data)

        self.assertEqual(e.observations, expected_observations)
