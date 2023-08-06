"""Contains helper functions for saving and loading experiments using the
json package.
"""

import os
import json
import binascii
import hashlib

import numpy as np
from researcher.globals import OBSERVATIONS_NAME
from researcher.experiment import Experiment

class TrickyValuesEncoder(json.JSONEncoder):
    """A JSON Encoder class that handles tricky python datatypes.
    """
    def default(self, obj):
        """Converts data types that the json package cannot handle into
        data types that it can.

        Args:
            obj (object): a python value that will be serialized by the 
            json package.

        Returns:
            object: The same value that was passed in represented as a 
            data type that the json package can serialize.
        """
        if isinstance(obj, np.float32):
            return float(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        
        return json.JSONEncoder.default(self, obj)

def get_hash(params):
    """Converts the given parameters deterministically into a unique hash. 

    Args:
        params (dict): The parameters that define an experiment.

    Returns:
        string: A hash that is deterministically generated from and unique
        to the given parameters.
    """
    return hex(int(binascii.hexlify(hashlib.md5(json.dumps(params, cls=TrickyValuesEncoder).encode("utf-8")).digest()), 16))[2:]

def save_experiment(path, name, parameters, observations):
    """Saves parameters and associated experiment observations to a JSON 
    file.

    Args:
        path (string): The parent directory in which to save the record.

        name (string): A short, somewhat human readable summary of the 
        experiment that is being saved.

        parameters (dict): The parameters that define the experimental 
        conditions of the experiment.

        observations (dict, optional): All observations made during the
        experiment.
    """
    file_name = path + name + ".json"

    experiment_dict = {**parameters, OBSERVATIONS_NAME: observations}

    with open(file_name, "w") as f:
        f.write(json.dumps(experiment_dict, indent=4, cls=TrickyValuesEncoder))

def all_experiments(path):
    """Loads all records in the given directory into Experiment instances.

    Args:
        path (string): The directory to search for experiment records to 
        load.

    Returns:
        list[Experiment]: All the experiments that were located
        in the given directory.
    """
    experiments = []
    for file in os.listdir(path):
        if file[-5:] == ".json":
            experiments.append(load_experiment(path, file))

    return sorted(experiments, key=lambda x: x.timestamp)

def past_experiment_from_hash(path, hash_segment):
    """Loads and returns the experiment which matches the given hash.

    Args:
        path (string): The directory to search for experiments in.

        hash_segment (string): At least 8 consecutive characters from the
        unique identifier hash of the sought experiment. 

    Raises:
        ValueError: If hash_segment is less than 8 characters long.
        ValueError: If more than one experiment that matches hash_segment
        was located.

        ValueError: If no experiments that match hash_segment were 
        located.

    Returns:
        Experiment: The experiment that matches hash_segment.
    """
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
    """Loads all experiments that match one of the given hashes.

    Args:
        path (string): The directory to search for experiments in.
        hash_segments (list[string]): Hashes that uniquely identify sought
        experiments.

    Returns:
        list[Experiment]: All experiments that were located 
        that match one of the given hashes.
    """
    return [past_experiment_from_hash(path, h) for h in hash_segments]

def load_experiment(path, name):
    """Loads and returns the data for an experiment.

    Args:
        path (string): The directory containing the experiment record.
        name (string): The full filename of the experiment record.

    Returns:
        researcher.Experiment: The data associated with that experiment
        including the experiment parameters and observations.
    """
    file_name = path + name

    if file_name[-5:] != ".json":
        file_name += ".json"

    with open(file_name, "r") as f:
        params = json.load(f)
    return Experiment(params)
