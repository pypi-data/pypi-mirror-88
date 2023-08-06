from researcher.dashboard import past_experiment_from_hash
from researcher.dashboard import *
import unittest

import numpy as np
import researcher as rs

from tests.tools import TEST_DATA_PATH

class TestDashboard(unittest.TestCase):
    def setUp(self):
        self.e = past_experiment_from_hash(TEST_DATA_PATH, "sadasd32823")
        self.e2 = past_experiment_from_hash(TEST_DATA_PATH, "6576g326g7112")
        self.e3 = past_experiment_from_hash(TEST_DATA_PATH, "7y2137h78123hhabsd8")

    def test_display_final_observations(self):

        final_compare([self.e], ["mse"])
        final_compare([self.e, self.e2], ["mse"])
   
    def test_plot_compare(self):
        plot_compare([self.e], ["mse"])
        plot_compare([self.e, self.e2], ["mse"])

    def test_plot_training(self):
        plot_training([self.e], ["mse"])
        plot_training([self.e, self.e2], ["mse"])

    def test_plot_folds(self):
        plot_folds([self.e], ["mse"])
        plot_folds([self.e3], ["batch_loss"])
        plot_folds([self.e, self.e2], ["mse"])

    def test_plot_progression(self):
        plot_lr(self.e3, "batch_loss", lr_name="learning_rate")
   