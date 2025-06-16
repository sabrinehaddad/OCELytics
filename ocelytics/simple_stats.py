"""
Provides basic statistics such as total number of objects and number of object variants.
"""

import inspect
from .feature import Feature
import pandas as pd

class SimpleStats(Feature):
    """
    Extracts basic summary statistics from the OCEL log.
    """

    def __init__(self, feature_names=None):
        self.feature_type = "simple_stats"
        super().__init__(feature_names)

    @classmethod
    def events(cls, ocel):
        """
        Convert OCEL events to a pandas DataFrame.

        Args:
            ocel (dict): The OCEL log.

        Returns:
            pd.DataFrame: Events DataFrame.
        """
        return pd.DataFrame.from_dict(ocel["ocel:events"], orient="index")

    @classmethod
    def objects(cls, ocel):
        """
        Convert OCEL objects to a pandas DataFrame.

        Args:
            ocel (dict): The OCEL log.

        Returns:
            pd.DataFrame: Objects DataFrame.
        """
        return pd.DataFrame.from_dict(ocel["ocel:objects"], orient="index")

    @classmethod
    def n_objects(cls, ocel):
        """
        Count total number of objects in the log.

        Returns:
            int: Total object count.
        """
        return len(cls.objects(ocel))

    @classmethod
    def n_object_variants(cls, ocel):
        """
        Count number of unique object activity sequences (variants).

        Returns:
            int: Count of unique variants.
        """
        events_df = cls.events(ocel)
        variants = {}

        for _, row in events_df.iterrows():
            activity = row["ocel:activity"]
            for obj_id in row["ocel:omap"]:
                variants.setdefault(obj_id, []).append(activity)

        unique_paths = set(tuple(path) for path in variants.values())
        return len(unique_paths)

    def extract(self, ocel):
        """
        Extract the simple statistics.

        Args:
            ocel (dict): OCEL log.

        Returns:
            dict: Selected features.
        """
        return {
            "n_objects": self.n_objects(ocel),
            "n_object_variants": self.n_object_variants(ocel),
        }
