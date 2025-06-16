"""
Extracts statistics related to event activities in the OCEL log.
"""

import inspect
import numpy as np
from collections import Counter
from scipy import stats
from .feature import Feature
import pandas as pd

class Activities(Feature):
    """
    Computes statistical metrics over activity occurrences.
    """

    def __init__(self, feature_names=None):
        self.feature_type = "activities"
        super().__init__(feature_names)

    @staticmethod
    def activities(ocel):
        """
        Count occurrences of each activity in the event log.
        """
        events_df = pd.DataFrame.from_dict(ocel["ocel:events"], orient="index")
        return Counter(events_df["ocel:activity"])

    @classmethod
    def n_unique_activities(cls, ocel): return len(cls.activities(ocel))
    @classmethod
    def activities_min(cls, ocel): return np.min(list(cls.activities(ocel).values()))
    @classmethod
    def activities_max(cls, ocel): return np.max(list(cls.activities(ocel).values()))
    @classmethod
    def activities_mean(cls, ocel): return np.mean(list(cls.activities(ocel).values()))
    @classmethod
    def activities_median(cls, ocel): return np.median(list(cls.activities(ocel).values()))
    @classmethod
    def activities_std(cls, ocel): return np.std(list(cls.activities(ocel).values()))
    @classmethod
    def activities_variance(cls, ocel): return np.var(list(cls.activities(ocel).values()))
    @classmethod
    def activities_q1(cls, ocel): return np.percentile(list(cls.activities(ocel).values()), 25)
    @classmethod
    def activities_q3(cls, ocel): return np.percentile(list(cls.activities(ocel).values()), 75)
    @classmethod
    def activities_iqr(cls, ocel): return stats.iqr(list(cls.activities(ocel).values()))

    @classmethod
    def activities_skewness(cls, ocel):
        """
        Compute skewness of activity frequency distribution.
        """
        values = list(cls.activities(ocel).values())
        if np.std(values) == 0:
            return 0.0
        return stats.skew(values)

    @classmethod
    def activities_kurtosis(cls, ocel):
        """
        Compute kurtosis of activity frequency distribution.
        """
        values = list(cls.activities(ocel).values())
        if np.std(values) == 0:
            return 0.0
        return stats.kurtosis(values)
