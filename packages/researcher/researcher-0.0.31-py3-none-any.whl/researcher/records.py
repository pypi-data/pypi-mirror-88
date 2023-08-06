import os
import json
import binascii
import hashlib
import datetime
from collections import defaultdict

import numpy as np
from researcher.globals import *

class Float32Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def get_hash(params):
    return hex(int(binascii.hexlify(hashlib.md5(json.dumps(params).encode("utf-8")).digest()), 16))[2:]

def save_experiment(path, name, parameters, results):
    file_name = path + name + ".json"
    with open(file_name, "w") as f:
        f.write(json.dumps({**parameters, **{"results": results}}, indent=4, cls=Float32Encoder))

def all_experiments(path):
    experiments = []
    for file in os.listdir(path):
        if file[-5:] == ".json":
            experiments.append(load_experiment(path, file))

    return sorted(experiments, key=lambda x: x.timestamp)


def past_experiment_from_hash(path, hash_segment):
    if len(hash_segment) < 8:
        raise ValueError("Hash segment {} must be at least 8 characters long to avoid ambiguity".format(hash_segment))

    past_experiments = [e for e in os.listdir(path) if e[-5:] == ".json"]
    experiment_name = None

    for e in past_experiments:
        if hash_segment in e:
            if experiment_name is not None:
                raise ValueError("At least two old experiments {} and {} found matching hash segment {}".format(experiment_name, e, hash_segment))
            experiment_name = e
    
    if not experiment_name:
        raise ValueError("Could not locate experiment for hash segment {} in directory {}".format(hash_segment, path))
    
    return load_experiment(path, experiment_name)

def past_experiments_from_hashes(path, hash_segments):
    return [past_experiment_from_hash(path, h) for h in hash_segments]

def load_experiment(path, name):
    file_name = path + name

    if file_name[-5:] != ".json":
        file_name += ".json"

    with open(file_name, "r") as f:
        params = json.load(f)
    return Experiment(params)

# ------------------------------------------------------------------------------
#
#                                   DATA CLASSES
#
# ------------------------------------------------------------------------------

class Experiment():
    def __init__(self, data):
        if data[RESULTS_NAME]:
            self.results = Results(data[RESULTS_NAME])
        else:
            self.results = None
        
        self.data = data
        self.timestamp = datetime.datetime.strptime(self.data["timestamp"], DATE_FORMAT)
    
    def is_trial(self):
        return "trial" in self.data and self.data["trial"]

    def get_hash(self):
        return self.data["hash"]

    def identifier(self):
        title =  self.data["title"] if "title" in self.data else ""

        id = "{}_{}".format(title, self.data["hash"][:8])

        if self.is_trial():
            id = "trial_" + id
        
        return id
    

VAL_PREFIX = "val_"

class Results():
    """Results provides an api to handle the collection and analysis of experiment results
    """
    def __init__(self, results=None):
        """ self.__results holds a mapping from each fold to each metric and from each metric to 
        all the recorded metric scores for that metric.
        fold -> metric -> [value, value, value, ...]
        """
        self.__results = results or []
    
    def __add_value(self, fold, name, value):
        self.__results[fold][name].append(value)

    def __integrate(self, fold, name):
        if len(self.__results) == fold:
            self.__results.append(defaultdict(lambda : []))
        if len(self.__results) < fold:
            raise ValueError("Attempt to write to fold {} when results {} only contains {} folds. It looks like a fold has been skipped".format(fold, self.__results, len(self.__results)))
        if len(self.__results) > fold + 1:
            raise ValueError("Attempt to write to fold {} when results {} contains {} folds already. We shouldn't be writing to already finalized folds.".format(fold, self.__results, len(self.__results)))

    def add(self, fold, name, value):
        self.__integrate(fold, name)
        self.__add_value(fold, name, value)

    def add_all(self, fold, name, values):
        self.__integrate(fold, name)

        for value in values:
            self.__add_value(fold, name, value)

    def get_metric(self, target_metric):
        return [metrics[target_metric] for metrics in self.__results]

    def has_metric(self, target_metric):
        # It is assumed that if a metric is in one fold it will be in every fold.
        # TODO: actually implement this constraint when metrics are being added.
        for metrics in self.__results:
            if not target_metric in metrics:
                return False
        return True

    def get_final_metric_value(self, target_metric):
        return [metrics[target_metric][-1] for metrics in self.__results]
    def get_final_val_metric_value(self, target_metric):
        return [metrics[VAL_PREFIX + target_metric][-1] for metrics in self.__results]

    def get_val_metric(self, target_metric):
        return [metrics[VAL_PREFIX + target_metric] for metrics in self.__results]

    def get_fold_aggregated_metric(self, target_metric, agg_fn):
        fold_wise = []
        for metrics in self.__results:
            fold_wise.append(metrics[target_metric][-1])

        return agg_fn(np.array(fold_wise), axis=0)
    
    def active_fold(self):
        return len(self.__results) - 1
    
    def view(self):
        return self.__results