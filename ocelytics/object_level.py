import inspect
import numpy as np
from collections import Counter
from .feature import Feature

class ObjectLevel(Feature):
    def __init__(self):
        super().__init__()
        self.feature_names = [
            "n_objects",
            "n_unique_object_types",
            "object_type_distribution",
            "min_events_per_object",
            "max_events_per_object",
            "mean_events_per_object",
            "median_events_per_object",
            "std_events_per_object",
            "variance_events_per_object",
            "q1_events_per_object",
            "q3_events_per_object"
        ]

    @staticmethod
    def objects(ocel):
        return ocel.get("ocel:objects", {})

    @staticmethod
    def events(ocel):
        return ocel.get("ocel:events", {})

    @classmethod
    def n_objects(cls, ocel):
        return len(cls.objects(ocel))

    @classmethod
    def n_unique_object_types(cls, ocel):
        obj_types = [obj.get("ocel:type") for obj in cls.objects(ocel).values()]
        return len(set(obj_types))

    @classmethod
    def _event_counts_per_object(cls, ocel):
        object_event_mapping = {}
        for event_data in cls.events(ocel).values():
            for obj_id in event_data.get("ocel:omap", []):
                object_event_mapping.setdefault(obj_id, []).append(event_data)
        return [len(events) for events in object_event_mapping.values()]

    @classmethod
    def min_events_per_object(cls, ocel):
        counts = cls._event_counts_per_object(ocel)
        return np.min(counts) if counts else None

    @classmethod
    def max_events_per_object(cls, ocel):
        counts = cls._event_counts_per_object(ocel)
        return np.max(counts) if counts else None

    @classmethod
    def mean_events_per_object(cls, ocel):
        counts = cls._event_counts_per_object(ocel)
        return np.mean(counts) if counts else None

    @classmethod
    def median_events_per_object(cls, ocel):
        counts = cls._event_counts_per_object(ocel)
        return np.median(counts) if counts else None

    @classmethod
    def std_events_per_object(cls, ocel):
        counts = cls._event_counts_per_object(ocel)
        return np.std(counts) if counts else None

    @classmethod
    def variance_events_per_object(cls, ocel):
        counts = cls._event_counts_per_object(ocel)
        return np.var(counts) if counts else None

    @classmethod
    def q1_events_per_object(cls, ocel):
        counts = cls._event_counts_per_object(ocel)
        return np.percentile(counts, 25) if counts else None

    @classmethod
    def q3_events_per_object(cls, ocel):
        counts = cls._event_counts_per_object(ocel)
        return np.percentile(counts, 75) if counts else None

    def extract(self, ocel):
        return {
            name: method(ocel)
            for name, method in inspect.getmembers(self.__class__, predicate=inspect.ismethod)
            if name in self.feature_names
        }


def extract(log):
    return ObjectLevel().extract(log)
