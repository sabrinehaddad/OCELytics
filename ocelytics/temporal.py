"""
Extracts time-based features from the OCEL log.

Includes total log duration, average time between events, and standard deviation of gaps.
"""

import inspect
from datetime import datetime
import numpy as np
from .feature import Feature

class Temporal(Feature):
    """
    Computes temporal statistics over event timestamps.
    """

    def __init__(self, feature_names=None):
        self.feature_type = "temporal"
        super().__init__(feature_names)

    @staticmethod
    def extract_timestamps(log):
        """
        Extract and sort all event timestamps from the OCEL log.

        Args:
            log (dict): The OCEL log.

        Returns:
            list[datetime]: Sorted list of event timestamps.
        """
        timestamps = []
        for event in log["ocel:events"].values():
            time_str = event.get("ocel:timestamp")
            if time_str:
                timestamps.append(datetime.fromisoformat(time_str))
        return sorted(timestamps)

    @classmethod
    def temporal_duration(cls, log):
        """
        Total time span covered by the log in seconds.

        Returns:
            float: Duration in seconds.
        """
        times = cls.extract_timestamps(log)
        return (times[-1] - times[0]).total_seconds() if times else 0

    @classmethod
    def temporal_avg_time_diff(cls, log):
        """
        Average time gap between consecutive events in seconds.

        Returns:
            float: Average time difference.
        """
        times = cls.extract_timestamps(log)
        if len(times) < 2:
            return 0
        diffs = [(t2 - t1).total_seconds() for t1, t2 in zip(times[:-1], times[1:])]
        return np.mean(diffs)

    @classmethod
    def temporal_std_time_diff(cls, log):
        """
        Standard deviation of time gaps between events in seconds.

        Returns:
            float: Standard deviation of time differences.
        """
        times = cls.extract_timestamps(log)
        if len(times) < 2:
            return 0
        diffs = [(t2 - t1).total_seconds() for t1, t2 in zip(times[:-1], times[1:])]
        return np.std(diffs)

    def extract(self, log):
        """
        Extract selected temporal features.

        Args:
            log (dict): The OCEL log.

        Returns:
            dict: Mapping of feature names to values.
        """
        return {
            name: method(log)
            for name, method in inspect.getmembers(self.__class__, predicate=inspect.ismethod)
            if name in self.feature_names
        }


def extract(log):
    return Temporal().extract(log)
