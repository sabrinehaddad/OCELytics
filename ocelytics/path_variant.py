import inspect
import numpy as np
from collections import defaultdict, Counter
from scipy import stats
from .feature import Feature

class PathVariant(Feature):
    def __init__(self, feature_names="path_variant"):
        self.feature_type = "path_variant"
        self.available_class_methods = dict(inspect.getmembers(PathVariant, predicate=inspect.ismethod))
        if self.feature_type in feature_names:
            self.feature_names = [*self.available_class_methods.keys()]
        else:
            self.feature_names = feature_names

    @staticmethod
    def object_variants(log):
        # Map object_id -> list of (timestamp, activity)
        object_paths = defaultdict(list)

        for event in log["ocel:events"].values():
            timestamp = event["ocel:timestamp"]
            activity = event["ocel:activity"]
            for obj_id in event["ocel:omap"]:
                object_paths[obj_id].append((timestamp, activity))

        # Sort each object's path by timestamp, extract only activities
        variant_sequences = []
        for obj_id, events in object_paths.items():
            sorted_acts = [act for _, act in sorted(events)]
            variant_sequences.append(tuple(sorted_acts))  # make it hashable

        return variant_sequences

    @staticmethod
    def occurrences(log):
        variants = PathVariant.object_variants(log)
        variant_counter = Counter(variants)
        return sorted(variant_counter.values(), reverse=True)

    @classmethod
    def ratio_most_common_variant(cls, log):
        occ = cls.occurrences(log)
        return occ[0] / len(log["ocel:objects"]) if occ else 0

    @classmethod
    def ratio_top_1_variants(cls, log):
        occ = cls.occurrences(log)
        cutoff = max(1, int(len(occ) * 0.01))
        return sum(occ[:cutoff]) / len(log["ocel:objects"])

    @classmethod
    def ratio_top_5_variants(cls, log):
        occ = cls.occurrences(log)
        cutoff = max(1, int(len(occ) * 0.05))
        return sum(occ[:cutoff]) / len(log["ocel:objects"])

    @classmethod
    def ratio_top_10_variants(cls, log):
        occ = cls.occurrences(log)
        cutoff = max(1, int(len(occ) * 0.10))
        return sum(occ[:cutoff]) / len(log["ocel:objects"])

    @classmethod
    def ratio_top_20_variants(cls, log):
        occ = cls.occurrences(log)
        cutoff = max(1, int(len(occ) * 0.20))
        return sum(occ[:cutoff]) / len(log["ocel:objects"])

    @classmethod
    def ratio_top_50_variants(cls, log):
        occ = cls.occurrences(log)
        cutoff = max(1, int(len(occ) * 0.50))
        return sum(occ[:cutoff]) / len(log["ocel:objects"])

    @classmethod
    def ratio_top_75_variants(cls, log):
        occ = cls.occurrences(log)
        cutoff = max(1, int(len(occ) * 0.75))
        return sum(occ[:cutoff]) / len(log["ocel:objects"])

    @classmethod
    def mean_variant_occurrence(cls, log):
        occ = cls.occurrences(log)
        return np.mean(occ) if occ else 0

    @classmethod
    def std_variant_occurrence(cls, log):
        occ = cls.occurrences(log)
        return np.std(occ) if occ else 0

    @classmethod
    def skewness_variant_occurrence(cls, log):
        occ = cls.occurrences(log)
        return stats.skew(occ) if len(occ) > 2 else 0

    @classmethod
    def kurtosis_variant_occurrence(cls, log):
        occ = cls.occurrences(log)
        return stats.kurtosis(occ) if len(occ) > 2 else 0

    def extract(self, log):
        return {
            name: method(log)
            for name, method in inspect.getmembers(self.__class__, predicate=inspect.ismethod)
            if name in self.feature_names
        }

# ✅ Entry point for CLI and feature_extractor
def extract(log):
    return PathVariant().extract(log)
