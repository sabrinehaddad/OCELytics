import inspect
import numpy as np
from collections import Counter
from scipy import stats
from .feature import Feature

class ActivitiesOCEL(Feature):
    def __init__(self):
        super().__init__()
        self.feature_names = [
            "n_unique_activities",
            "activities_min",
            "activities_max",
            "activities_mean",
            "activities_median",
            "activities_std",
            "activities_variance",
            "activities_q1",
            "activities_q3",
            "activities_iqr",
            "activities_skewness",
            "activities_kurtosis"
        ]

    @staticmethod
    def activities(ocel):
        return Counter(event["ocel:activity"] for event in ocel["ocel:events"].values())

    @classmethod
    def n_unique_activities(cls, ocel):
        return len(cls.activities(ocel))

    @classmethod
    def activities_min(cls, ocel):
        return np.min(list(cls.activities(ocel).values()))

    @classmethod
    def activities_max(cls, ocel):
        return np.max(list(cls.activities(ocel).values()))

    @classmethod
    def activities_mean(cls, ocel):
        return np.mean(list(cls.activities(ocel).values()))

    @classmethod
    def activities_median(cls, ocel):
        return np.median(list(cls.activities(ocel).values()))

    @classmethod
    def activities_std(cls, ocel):
        return np.std(list(cls.activities(ocel).values()))

    @classmethod
    def activities_variance(cls, ocel):
        return np.var(list(cls.activities(ocel).values()))

    @classmethod
    def activities_q1(cls, ocel):
        return np.percentile(list(cls.activities(ocel).values()), 25)

    @classmethod
    def activities_q3(cls, ocel):
        return np.percentile(list(cls.activities(ocel).values()), 75)

    @classmethod
    def activities_iqr(cls, ocel):
        return stats.iqr(list(cls.activities(ocel).values()))

    @classmethod
    def activities_skewness(cls, ocel):
        return stats.skew(list(cls.activities(ocel).values()))

    @classmethod
    def activities_kurtosis(cls, ocel):
        return stats.kurtosis(list(cls.activities(ocel).values()))

    def extract(self, ocel):
        return {
            name: method(ocel)
            for name, method in inspect.getmembers(self.__class__, predicate=inspect.ismethod)
            if name in self.feature_names
        }


def extract(log):
    return ActivitiesOCEL().extract(log)
