"""
Extracts statistics about the last activities in each object lifecycle from the OCEL log.
"""

import numpy as np
from scipy import stats
from .feature import Feature

class EndActivities(Feature):
    """
    Computes statistical metrics over end activities of object lifecycles.
    """

    def __init__(self, feature_names=None):
        self.feature_type = "end_activities"
        super().__init__(feature_names)

        self.available_class_methods = {
            fname: getattr(self, fname)
            for fname in dir(self)
            if not fname.startswith("_") and callable(getattr(self, fname)) and fname.startswith(("end_", "n_unique"))
        }

    @staticmethod
    def get_end_activities(log):
        """
        Extract the last activity for each object's lifecycle.

        Args:
            log (dict): Parsed OCEL log.

        Returns:
            list: A list of end activity labels.
        """
        events = sorted(log["ocel:events"].values(), key=lambda e: e["ocel:timestamp"])
        object_traces = {}
        for event in events:
            for obj in event.get("ocel:omap", []):
                object_traces.setdefault(obj, []).append(event)
        return [trace[-1]["ocel:activity"] for trace in object_traces.values() if trace]

    @staticmethod
    def _activity_counts(activities):
        """
        Count how often each end activity occurs.

        Args:
            activities (list): End activities.

        Returns:
            list[int]: Frequency of each end activity.
        """
        counts = {}
        for act in activities:
            counts[act] = counts.get(act, 0) + 1
        return list(counts.values())

    # Statistical summaries
    @classmethod
    def n_unique_end_activities(cls, log): return len(set(cls.get_end_activities(log)))
    @classmethod
    def end_activities_min(cls, log): return np.min(cls._activity_counts(cls.get_end_activities(log)))
    @classmethod
    def end_activities_max(cls, log): return np.max(cls._activity_counts(cls.get_end_activities(log)))
    @classmethod
    def end_activities_mean(cls, log): return np.mean(cls._activity_counts(cls.get_end_activities(log)))
    @classmethod
    def end_activities_median(cls, log): return np.median(cls._activity_counts(cls.get_end_activities(log)))
    @classmethod
    def end_activities_std(cls, log): return np.std(cls._activity_counts(cls.get_end_activities(log)))
    @classmethod
    def end_activities_variance(cls, log): return np.var(cls._activity_counts(cls.get_end_activities(log)))
    @classmethod
    def end_activities_q1(cls, log): return np.percentile(cls._activity_counts(cls.get_end_activities(log)), 25)
    @classmethod
    def end_activities_q3(cls, log): return np.percentile(cls._activity_counts(cls.get_end_activities(log)), 75)
    @classmethod
    def end_activities_iqr(cls, log): return stats.iqr(cls._activity_counts(cls.get_end_activities(log)))
    @classmethod
    def end_activities_skewness(cls, log): return stats.skew(cls._activity_counts(cls.get_end_activities(log)))
    @classmethod
    def end_activities_kurtosis(cls, log): return stats.kurtosis(cls._activity_counts(cls.get_end_activities(log)))
