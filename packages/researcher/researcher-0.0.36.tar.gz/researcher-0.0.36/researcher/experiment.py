import datetime

from researcher.globals import DATE_FORMAT, OBSERVATIONS_NAME
from researcher.observations import FinalizedObservations

class Experiment(FinalizedObservations):
    """Contains all the data related to a single recorded experiment.

    Attributes:
        data (dict): All information, observations as well as parameters, 
        associated with the recorded experiment.

        timestamp: (datetime.datetime) The time at which the recorded 
        experiment was first recorded.
    """
    def __init__(self, data):
        """Instantiates an Experiment.

        Args:
            data (dict): all recorded data relating to an experiment. This
            includes experimental parameters as well as observations.
        """
        if OBSERVATIONS_NAME in data:
            observations = data[OBSERVATIONS_NAME]
        else:
            observations = {}

        super().__init__(observations)
        
        self.data = data

        self.timestamp = datetime.datetime.strptime(self.data["timestamp"], DATE_FORMAT) if "timestamp" in self.data else None
        

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
        
        return id