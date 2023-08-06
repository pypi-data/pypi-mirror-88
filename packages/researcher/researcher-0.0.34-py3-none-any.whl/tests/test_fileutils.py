
import unittest
import json

import numpy as np
import researcher as rs

from tests.tools import TEST_DATA_PATH

class TestFileUtils(unittest.TestCase):
    def test_does_not_mutate_params(self):
        params = {"a": 4, "b": 8, "c": [5, 6, 7, ]}
        expected = {"a": 4, "b": 8, "c": [5, 6, 7, ]}

        rs.save_experiment(TEST_DATA_PATH, "somename", params, {"loss": [0.1, 0.4, 0.231]})

        self.assertDictEqual(params, expected)

    def test_handles_floats(self):
        params = {"a": 4, "b": 8, "c": [5, 6, 7, ]}

        rs.save_experiment(TEST_DATA_PATH, "somename", params, fold_results={"loss": [np.float32(0.1), 0.4, 0.231]})

    def test_saves_correctly(self):
        params = {"a": 4, "b": 8, "c": [5, 6, 7, ]}
        expected = {"a": 4, "b": 8, "c": [5, 6, 7, ], "results": {"fold_results": {"loss": [0.1, 0.4, 0.231]}}}

        rs.save_experiment(TEST_DATA_PATH, "somename", params, fold_results={"loss": [0.1, 0.4, 0.231]})

        with open(TEST_DATA_PATH + "somename.json") as f:
            saved = json.load(f)

        self.assertDictEqual(saved, expected)

    def test_saves_general_results_correctly(self):
        params = {"a": 4, "b": 8, "c": [5, 6, 7]}
        expected = {"a": 4, "b": 8, "c": [5, 6, 7], "results": {"general_results": {"loss": [0.1, 0.4, 0.231]}}}

        rs.save_experiment(TEST_DATA_PATH, "somename", params, general_results={"loss": [0.1, 0.4, 0.231]})

        with open(TEST_DATA_PATH + "somename.json") as f:
            saved = json.load(f)

        self.assertDictEqual(saved, expected)