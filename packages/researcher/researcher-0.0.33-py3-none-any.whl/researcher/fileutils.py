import os
import json
import binascii
import hashlib
import math

import numpy as np
from researcher.globals import RESULTS_NAME, GENERAL_RESULTS_NAME, FOLD_RESULTS_NAME
from researcher.experiment import Experiment

class TrickyValuesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        
        return json.JSONEncoder.default(self, obj)

def get_hash(params):
    return hex(int(binascii.hexlify(hashlib.md5(json.dumps(params, cls=TrickyValuesEncoder).encode("utf-8")).digest()), 16))[2:]

def save_experiment(path, name, parameters, fold_results=None, general_results=None):
    file_name = path + name + ".json"

    result_dict = {}
    experiment_dict = {**parameters, RESULTS_NAME: result_dict}
    if fold_results is not None:
        result_dict[FOLD_RESULTS_NAME] = fold_results
    if general_results is not None:
        result_dict[GENERAL_RESULTS_NAME] = general_results

    with open(file_name, "w") as f:
        f.write(json.dumps(experiment_dict, indent=4, cls=TrickyValuesEncoder))

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
