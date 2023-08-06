"""Contains functions to save experiment parameters and results more easily.
"""

import datetime
import os
import copy

from researcher.fileutils import *
from researcher.globals import *

def reduced_params(params, unwanted_keys):
    """Create a copy of params with the selected fields removed.

    Args:
        params (dict): The parameters that define an experiment which may 
        or may not have been run already.

        unwanted_keys (list[string]): The fields to remove.

    Returns:
        dict: A copy of the original parameters minus the selected keys.
    """
    if not isinstance(unwanted_keys, set):
        unwanted_keys = set(unwanted_keys)

    return {k: params[k] for k in params.keys() - unwanted_keys}

def record_experiment_with_collector(params, save_path, collector=None, duration=None):
    """Saves the experiment parameters and observations by unpacking those 
    observations from a researcher.ObservationCollector instance.

    Args:
        params (dict): The parameters that define the experimental 
        conditions of the experiment.

        save_path (string): The parent directory in which to save 
        experimental observations.
        
        collector (researcher.ObservationCollector, optional): An object 
        which contains the observations collected during the experiment.
        Defaults to None.

        duration (datetime.timedelta, optional): The time elapsed between
        the start and the end of the experiment. Defaults to None.
    """
    observations = collector.observations if collector is not None else None

    record_experiment(params, save_path, observations, duration)

def record_experiment(params, save_path, observations=None, duration=None):
    """Saves the parameters and associated experiment observations to a 
    JSON experiment record.

    Args:
        params (dict): The parameters that define the experimental 
        conditions of the experiment.

        save_path (string): The parent directory in which to save 
        experiment observations.

        observations (dict, optional): The observations made during the
        experiment. Defaults to None.

        duration (datetime.timedelta, optional): The time elapsed between
        the start and the end of the experiment. Defaults to None.
    """
    if not os.path.isdir(save_path):
        os.mkdir(save_path)

    cloned_params = copy.deepcopy(params)
    param_hash = get_hash(cloned_params)

    cloned_params["hash"] = param_hash
    cloned_params["timestamp"] = datetime.datetime.now().strftime(DATE_FORMAT)

    if duration is not None:
        cloned_params["duration"] = duration.total_seconds()

    if "title" in cloned_params:
        title = cloned_params["title"]
    else:
        title = "no_title"

    save_experiment(save_path, "{}_{}".format(title, param_hash), parameters=cloned_params, observations=observations)

