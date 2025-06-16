"""
Extracts statistics related to objects and object types in the OCEL log.
"""

import inspect
import numpy as np
from collections import Counter
from .feature import Feature
import pandas as pd

class Objects(Feature):
    """
    Computes object-level statistics from the OCEL log, such as number of objects and types.
    """

    def __init__(self, feature_names=None):
        self.feature_type = "objects"
        super().__init__(feature_names)

    @staticmethod
    def objects(ocel):
        """
        Convert the object section of the OCEL log into a DataFrame.

        Args:
            ocel (dict): The OCEL log.

        Returns:
            pd.DataFrame: DataFrame of objects with their types and properties.
        """
        return pd.DataFrame.from_dict(ocel["ocel:objects"], orient="index")

    @classmethod
    def n_objects(cls, ocel):
        """
        Count total number of objects in the log.

        Returns:
            int: Number of objects.
        """
        return len(cls.objects(ocel))

    @classmethod
    def n_object_types(cls, ocel):
        """
        Count unique object types in the log.

        Returns:
            int: Number of distinct object types.
        """
        return cls.objects(ocel)["ocel:type"].nunique()

    def extract(self, ocel):
        """
        Extract only the selected object-level features.

        Args:
            ocel (dict): OCEL log.

        Returns:
            dict: Mapping of feature names to values.
        """
        return {
            name: method(ocel)
            for name, method in inspect.getmembers(self.__class__, predicate=inspect.ismethod)
            if name in self.feature_names
        }
