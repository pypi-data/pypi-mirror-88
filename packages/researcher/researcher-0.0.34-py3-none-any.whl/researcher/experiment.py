import datetime

from researcher.globals import DATE_FORMAT, RESULTS_NAME, GENERAL_RESULTS_NAME, FOLD_RESULTS_NAME
from researcher.results import FinalizedResults

class Experiment(FinalizedResults):
    """Contains all the data related to a single recorded experiment.

    Attributes:
        fold_results (dict): The per-fold results of the recorded 
        experiment, assuming the experiment in question involved folds.

        general_results (dict): Any additional results related to the 
        recorded experiment that are not related to any particular fold.

        data (dict): All information, results as well as parameters, 
        associated with the recorded experiment.

        timestamp: (datetime.datetime) The time at which the recorded 
        experiment was first recorded.
    """
    def __init__(self, data):
        """Instantiates an Experiment.

        Args:
            data (dict): all recorded data relating to an experiment. This
            includes experimental parameters as well as results.
        """
        if RESULTS_NAME in data:
            results = data[RESULTS_NAME]

            fold_results = results[FOLD_RESULTS_NAME] if FOLD_RESULTS_NAME in results else None
            general_results = results[GENERAL_RESULTS_NAME] if GENERAL_RESULTS_NAME in results else None
        else:
            fold_results = None
            general_results = None

        super().__init__(fold_results, general_results)
        
        self.data = data
        self.timestamp = datetime.datetime.strptime(self.data["timestamp"], DATE_FORMAT)

    def get_hash(self):
        """Returns the unique identifier of the given experiment.

        Returns:
            string: The unique identifier for this experiment.
        """
        return self.data["hash"]

    def identifier(self):
        """Returns a human-friendly summary identifier for the experiment.
        This summary describes the experiment somewhat and is also unlikely
        to be shared between two different experiments.

        Returns:
            string: A somewhat unique, somewhat human readable experiment 
            identifier.
        """
        title = self.data["title"] + "_" if "title" in self.data else ""

        id = title + self.data["hash"][:8]

        if self.is_trial():
            id = "trial_" + id
        
        return id