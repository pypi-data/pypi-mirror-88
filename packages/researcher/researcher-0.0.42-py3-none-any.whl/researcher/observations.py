from researcher.globals import *

class Observations():
    """A light wrapper around experiment observations.

    Attributes:
        observations (dict, optional): All observations made during the experiment.
    """
    def __init__(self, observations=None):
        self.observations = observations if observations else {}

class ObservationCollector(Observations):
    """Makes the task of collecting experiment observations easier.
    """
    def __init__(self):
        super().__init__(None)

        self.__fold_data = set()
        self.__non_fold_data = set()

    def __add_fold_value(self, fold, key, value):
        self.observations[key][fold].append(value)

    def __add_fold(self, fold, key):
        if not key in self.observations:
            self.observations[key] = []
            self.__fold_data.add(key)
        
        while len(self.observations[key]) <= fold:
            self.observations[key].append([])

    def add_tensorflow_history(self, fold, history):
        """Adds all the data in a tensorflow History instance to the 
        specified fold.

        Args:
            fold (int): The fold to add data to.

            history (tensorflow.keras.callbacks.History): A record of the
            training loss values and metrics recorded during the training
            of a tensorflow model.
        """
        for key, values in history.history.items():
            self.add_multiple(fold, key, values)

    def set_observation(self, key, value):
        """Stores the specified values under the specified key. 

        Args:
            key (string): The type of data being logged, e.g.: "f1_score"
            or  "loss". 

            value (object): The observations to store under the given key.

        Raises:
            ValueError: If the given key is already being used to store values.
        """
        if key in self.observations:
            raise ValueError(f"key {key} is already being used to store the following observations: {self.observations[key]}")

        self.__non_fold_data.add(key)
        self.observations[key] = value

    def set_observations(self, obs_dict):
        """Stores the whole dictionary of data as experiment observations.

        Args:
            obs_dict (dict): A dictionatry containing data collected 
            during an experiment.
        """
        for key, value in obs_dict.items():
            self.set_observation(key, value)

    def add_fold_observation(self, fold, key, value):
        """Appends the given value to the list of values associated with 
        the specified field in the specified fold. For instance, you might
        call this method to continuously add datapoints to the accuracy 
        metric for each fold as training progresses. You cannot add fold
        data to a key if it already holds non-fold data.

        Args:
            fold (int): The fold to add data to. The first fold is fold 0.

            key (string): The name of the data being logged, e.g.:
            "f1_score" or  "loss". 

            value (object): The next value to add to the data for this 
            fold. Usually a float.
        Raises:
            ValueError: If the specified key is already storing non-fold
            related observations.
        """
        if key in self.__non_fold_data:
            raise ValueError(f"Cannot add fold data to {key}, since this key is already being used to store non-fold related observations")

        self.__add_fold(fold, key)
        self.__add_fold_value(fold, key, value)

    def add_fold_observations(self, fold, key, values):
        """Appends multiple values to the list of values associated with 
        the specified field in the specified fold.

        Args:
            fold (int): The fold to add data to.

            key (string): The name of the data being logged, e.g.:
            "f1_score" or  "loss".

            values (list[object]): The next values to add to the data for this 
            fold. Usually a list of floats.
        """
        if key in self.__non_fold_data:
            raise ValueError(f"Cannot add fold data to {key}, since this key is already being used to store non-fold related observations")

        self.__add_fold(fold, key)
        for value in values:
            self.__add_fold_value(fold, key, value)

class FinalizedObservations(Observations):
    """Observations loaded from an already completed experiment. 
    """
    def __init__(self, observations):
        super().__init__(observations)

    def has_observation(self, key):
        """
        Args:
            key (string): A name that is expected to be associated with
            some data collected from the experiment.

        Returns:
            bool: An indicator of whether there is any data associated with the 
            specified key stored in the experiment observations.
        """
        return key in self.observations

    def final_observations(self, key):
        """Identifies the values associated with the specified key and
        returns the last recorded value. If the key is associated with
        more than one fold, the last values of each fold are returned.

        Args:
            key (string): A name that is expected to be associated with
            some fold-related data collected from the experiment.

        Returns:
            object: The last recorded datapoint for the specified name for
            each fold.

        Raises:
            ValueError: If the specified key is not associated with a list
            of values.

            ValueError: If the specified key is associated with an empty 
            list.
        """
        values = self.observations[key]

        if not isinstance(values, list):
            raise ValueError(f"expected key {key} to be associated with a list of observations, got {values}")
        
        if len(values) == 0:
            raise ValueError(f"expected key {key} to have some values associated with it, got {values}")

        if isinstance(values[0], list):
            return [fold[-1] for fold in values]

        return values[-1]