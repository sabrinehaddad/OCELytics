import inspect
import numpy as np
from collections import Counter
from scipy import stats
from .feature import Feature

class Activities(Feature):
    def __init__(self, feature_names=None):
        self.feature_type = "activities"
        self.available_class_methods = dict(inspect.getmembers(self.__class__, predicate=inspect.ismethod))

        if feature_names is None or self.feature_type in feature_names:
            self.feature_names = list(self.available_class_methods.keys())
        else:
            self.feature_names = feature_names

    @staticmethod
    def activities(ocel):
      return Counter(event["ocel:activity"] for _, event in ocel.events.iterrows())

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
