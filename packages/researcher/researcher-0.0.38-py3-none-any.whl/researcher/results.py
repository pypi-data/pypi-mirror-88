"""Contains classes to better manage experiment result data, both while
collecting it for recording and loading it for analysis.
"""

from collections import defaultdict

import numpy as np

from researcher.globals import *

class Results():
    """A light wrapper around experiment results.

    Attributes:
        fold_results (dict): The per-fold results of the recorded 
        experiment, assuming the experiment in question involved folds.

        general_results (dict): Any additional results related to the 
        recorded experiment that are not related to any particular fold.
    """
    def __init__(self, fold_results=None, general_results=None):
        self.general_results = general_results if general_results is not None else {}
        self.fold_results = fold_results if fold_results is not None else []

class ResultBuilder(Results):
    """Makes the task of gathering and saving experiment results easier.

    Attributes:
        fold_results (dict): The per-fold results of the recorded 
        experiment, assuming the experiment in question involved folds.

        general_results (dict): Any additional results related to the 
        recorded experiment that are not related to any particular fold.
    """
    def __init__(self):
        super().__init__(None, None)

        self.__fold_metric_names = set()

    def __add_fold_value(self, fold, name, value):
        self.fold_results[fold][name].append(value)

    def __integrate(self, fold, name):
        if len(self.fold_results) == fold:
            self.fold_results.append(defaultdict(lambda : []))
        if len(self.fold_results) < fold:
            raise ValueError("Attempt to write to fold {} when results {} only contains {} folds. It looks like a fold has been skipped".format(fold, self.fold_results, len(self.fold_results)))
        if len(self.fold_results) > fold + 1:
            raise ValueError("Attempt to write to fold {} when results {} contains {} folds already. We shouldn't be writing to already finalized folds.".format(fold, self.fold_results, len(self.fold_results)))

    def set_general_metric(self, name, value):
        """Sets the value of a field in general (non fold-related) results
        to the given value. If the specified name already has 
        associated data in general results or any fold, an error 
        will be raised.

        Args:
            name (string): The field to set.
            value (object): The value to store. 
        """
        self.add(GENERAL_RESULTS_NAME, name, value)

    def set_general_metrics(self, result_dict):
        """Saves the given dictionary to the pool of general (non 
        fold-related) results. If the specified name already has 
        associated data in general results or any fold, an error 
        will be raised.

        Args:
            result_dict (dict): A dictionary of general results to save.
        """
        for key, value in result_dict.items():
            self.add(GENERAL_RESULTS_NAME, key, value)

    def add(self, fold, name, value):
        """Appends the given value to the list of values associated with 
        the specified field in the specified fold. For instance, you might
        call this method to continuously add datapoints to the accuracy 
        metric for each fold as training progresses. You cannot add a name
        to the fold results if it already exists in general results or
        vise versa.

        Args:
            fold (int): The fold to add data to (usually the current 
            fold). Set fold=none or fold="general_results" to add to the
            general results pool instead.

            name (string): The name of the data being logged, e.g.:
            "f1_score" or  "loss". 

            value (object): The next value to add to the data for this 
            fold. Usually a float.
        Raises:
            ValueError: If the specified fold is general results and the 
            specified name already exists in fold results.

            ValueError: If the specified fold is general results and the 
            specified name name already has associated data in general 
            results.

            ValueError: If the specified fold is not general results and 
            the specified name already holds data in general results.

        """
        if fold is None or fold == GENERAL_RESULTS_NAME:
            if name in  self.__fold_metric_names:
                raise ValueError(f"metric name {name} has already been given to a fold metric {self.fold_results}, adding it to general results")
            if name in self.general_results.keys():
                raise ValueError(f"metric name {name} already exists in general results: {self.general_results}")
            
            self.general_results[name] = value

        else:
            if name in self.general_results.keys():
                raise ValueError(f"metric name {name} already exists in general results {self.general_results}, adding it to the results fold {fold} would create ambiguity")
            self.__integrate(fold, name)
            self.__add_fold_value(fold, name, value)
            self.__fold_metric_names.add(name)

    def add_multiple(self, fold, name, values):
        """Appends multiple values to the list of values associated with 
        the specified field in the specified fold.

        Args:
            fold (int): The fold to add data to (usually the current 
            fold).

            name (string): The name of the data being logged, e.g.:
            "f1_score" or  "loss".

            values (list[object]): The next values to add to the data for this 
            fold. Usually a list of floats.
        """
        self.__integrate(fold, name)

        for value in values:
            self.__add_fold_value(fold, name, value)

    def active_fold(self):
        """
        Returns:
            int: The index of the highest fold added to so far.
        """
        return len(self.fold_results) - 1

class FinalizedResults(Results):
    """Results loaded from an already completed and recorded experiment. 
    """
    def __init__(self, fold_results, general_results):
        super().__init__(fold_results, general_results)

    def get_metric(self, name):
        """Returns the general or fold result values associated with the
        specified name. If there is data for that name in both general and
        fold results, then only the general result data will be returned.

        Args:
            name (string): The name of the data to be returned. Often a 
            metric like "loss" or "accuracy".

        Returns:
            object: The data associated with the specified name.
        """
        if name in self.general_results:
            return self.general_results[name]

        return [metrics[name] for metrics in self.fold_results]

    def has_metric(self, name):
        """
        Args:
            name (string): A name that is expected to be associated with
            some data collected from the experiment.

        Returns:
            bool: An indicator of whether there is any data associated with the 
            specified name stored in the experiment results.
        """
        if name in self.general_results:
            return True

        # It is assumed that if a metric is in one fold it will be in every fold.
        # TODO: actually implement this constraint when metrics are being added.
        for metrics in self.fold_results:
            if not name in metrics:
                return False
        return True

    def get_final_metric_values(self, name):
        """Identifies the values in each fold associated with the 
        specified name and returns the last recorded value for each fold.

        Args:
            name (string): A name that is expected to be associated with
            some fold-related data collected from the experiment.

        Returns:
            object: The last recorded datapoint for the specified name for
            each fold.
        """
        return [metrics[name][-1] for metrics in self.fold_results]

    def get_fold_aggregated_metric(self, name, agg_fn):
        """Aggregates the data associated with the specified name over all
        folds using the specified function and returns the aggregation.

        Args:
            name (string): A name that is expected to be associated with
            some fold-related data collected from the experiment.

            agg_fn (Callable): A function that can be used to aggregate 
            numpy arrays.

        Returns:
            numpy.ndarray: The data associated with the specified name 
            aggregated accross all folds.
        """
        fold_wise = []
        for metrics in self.fold_results:
            fold_wise.append(metrics[name])

        return agg_fn(np.array(fold_wise), axis=0)
    

