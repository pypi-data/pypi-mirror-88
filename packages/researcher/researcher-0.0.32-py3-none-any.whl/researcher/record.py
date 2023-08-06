import datetime
import os
import time
import gc
import json
import copy

import numpy as np

from researcher.fileutils import *
from researcher.globals import *
from researcher.results import Results

def reduced_params(params, unwanted_keys):
    """Create a copy of the given parameters without descriptive (human-directed) fields.
    """

    if not isinstance(unwanted_keys, set):
        unwanted_keys = set(unwanted_keys)

    return {k: params[k] for k in params.keys() - unwanted_keys}


def record_experiment_with_result_builder(params, save_path, result_builder=None, duration=None):
    fold_results = result_builder.fold_results if result_builder is not None else None
    general_results = result_builder.general_results if result_builder is not None else None

    record_experiment(params, save_path, fold_results, general_results, duration)

def record_experiment(params, save_path, fold_results=None, general_results=None, duration=None):
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

    save_experiment(save_path, "{}_{}".format(title, param_hash), parameters=cloned_params, fold_results=fold_results, general_results=general_results)

