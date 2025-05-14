import inspect
import numpy as np
from collections import defaultdict, Counter
from scipy import stats
from .feature import Feature

class PathVariant(Feature):
    def __init__(self, feature_names=None):
        self.feature_type = "path_variant"
        self.available_class_methods = dict(inspect.getmembers(self.__class__, predicate=inspect.ismethod))

        if feature_names is None or self.feature_type in feature_names:
            self.feature_names = list(self.available_class_methods.keys())
        else:
            self.feature_names = feature_names

    @staticmethod
    def object_variants(ocel):
        object_paths = defaultdict(list)

        for event in ocel["ocel:events"].values():
            timestamp = event["ocel:timestamp"]
            activity = event["ocel:activity"]
            for obj_id in event.get("ocel:omap", []):
                object_paths[obj_id].append((timestamp, activity))

        variant_sequences = [
            tuple(act for _, act in sorted(events))
            for events in object_paths.values()
        ]

        return variant_sequences

    @classmethod
    def occurrences(cls, ocel):
        variants = cls.object_variants(ocel)
        variant_counter = Counter(variants)
        return sorted(variant_counter.values(), reverse=True)

    @classmethod
    def ratio_most_common_variant(cls, ocel):
        occ = cls.occurrences(ocel)
        return occ[0] / len(ocel["ocel:objects"]) if occ else 0

    @classmethod
    def ratio_top_1_variants(cls, ocel):
        occ = cls.occurrences(ocel)
        cutoff = max(1, int(len(occ) * 0.01))
        return sum(occ[:cutoff]) / len(ocel["ocel:objects"])

    @classmethod
    def ratio_top_5_variants(cls, ocel):
        occ = cls.occurrences(ocel)
        cutoff = max(1, int(len(occ) * 0.05))
        return sum(occ[:cutoff]) / len(ocel["ocel:objects"])

    @classmethod
    def ratio_top_10_variants(cls, ocel):
        occ = cls.occurrences(ocel)
        cutoff = max(1, int(len(occ) * 0.10))
        return sum(occ[:cutoff]) / len(ocel["ocel:objects"])

    @classmethod
    def ratio_top_20_variants(cls, ocel):
        occ = cls.occurrences(ocel)
        cutoff = max(1, int(len(occ) * 0.20))
        return sum(occ[:cutoff]) / len(ocel["ocel:objects"])

    @classmethod
    def ratio_top_50_variants(cls, ocel):
        occ = cls.occurrences(ocel)
        cutoff = max(1, int(len(occ) * 0.50))
        return sum(occ[:cutoff]) / len(ocel["ocel:objects"])

    @classmethod
    def ratio_top_75_variants(cls, ocel):
        occ = cls.occurrences(ocel)
        cutoff = max(1, int(len(occ) * 0.75))
        return sum(occ[:cutoff]) / len(ocel["ocel:objects"])

    @classmethod
    def mean_variant_occurrence(cls, ocel):
        occ = cls.occurrences(ocel)
        return np.mean(occ) if occ else 0

    @classmethod
    def std_variant_occurrence(cls, ocel):
        occ = cls.occurrences(ocel)
        return np.std(occ) if occ else 0

    @classmethod
    def skewness_variant_occurrence(cls, ocel):
        occ = cls.occurrences(ocel)
        return stats.skew(occ) if len(occ) > 2 else 0

    @classmethod
    def kurtosis_variant_occurrence(cls, ocel):
        occ = cls.occurrences(ocel)
        return stats.kurtosis(occ) if len(occ) > 2 else 0

    def extract(self, ocel):
        return {
            name: method(ocel)
            for name, method in inspect.getmembers(self.__class__, predicate=inspect.ismethod)
            if name in self.feature_names
        }
