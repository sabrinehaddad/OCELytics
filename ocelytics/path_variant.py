"""
Analyzes object execution variants based on their activity sequences.

Computes frequency-based metrics and statistical summaries over variant distributions.
"""

import inspect
import numpy as np
from collections import defaultdict, Counter
from scipy import stats
from .feature import Feature

class PathVariant(Feature):
    """
    Computes statistics related to execution path variants across objects.
    """

    def __init__(self, feature_names=None):
        self.feature_type = "path_variant"
        super().__init__(feature_names)

    @staticmethod
    def object_variants(ocel):
        """
        Extract the sequence of activities per object.

        Args:
            ocel (dict): The OCEL log.

        Returns:
            list[tuple]: List of ordered activity tuples (variants) per object.
        """
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
        """
        Count how many times each variant occurs.

        Returns:
            list[int]: Sorted list of variant frequencies.
        """
        variants = cls.object_variants(ocel)
        variant_counter = Counter(variants)
        return sorted(variant_counter.values(), reverse=True)

    # Ratio-based metrics for top variants
    @classmethod
    def ratio_most_common_variant(cls, ocel): return cls.occurrences(ocel)[0] / len(ocel["ocel:objects"]) if cls.occurrences(ocel) else 0
    @classmethod
    def ratio_top_1_variants(cls, ocel): return sum(cls.occurrences(ocel)[:max(1, int(len(cls.occurrences(ocel)) * 0.01))]) / len(ocel["ocel:objects"])
    @classmethod
    def ratio_top_5_variants(cls, ocel): return sum(cls.occurrences(ocel)[:max(1, int(len(cls.occurrences(ocel)) * 0.05))]) / len(ocel["ocel:objects"])
    @classmethod
    def ratio_top_10_variants(cls, ocel): return sum(cls.occurrences(ocel)[:max(1, int(len(cls.occurrences(ocel)) * 0.10))]) / len(ocel["ocel:objects"])
    @classmethod
    def ratio_top_20_variants(cls, ocel): return sum(cls.occurrences(ocel)[:max(1, int(len(cls.occurrences(ocel)) * 0.20))]) / len(ocel["ocel:objects"])
    @classmethod
    def ratio_top_50_variants(cls, ocel): return sum(cls.occurrences(ocel)[:max(1, int(len(cls.occurrences(ocel)) * 0.50))]) / len(ocel["ocel:objects"])
    @classmethod
    def ratio_top_75_variants(cls, ocel): return sum(cls.occurrences(ocel)[:max(1, int(len(cls.occurrences(ocel)) * 0.75))]) / len(ocel["ocel:objects"])

    # Statistical summaries
    @classmethod
    def mean_variant_occurrence(cls, ocel): return np.mean(cls.occurrences(ocel)) if cls.occurrences(ocel) else 0
    @classmethod
    def std_variant_occurrence(cls, ocel): return np.std(cls.occurrences(ocel)) if cls.occurrences(ocel) else 0
    @classmethod
    def skewness_variant_occurrence(cls, ocel): return stats.skew(cls.occurrences(ocel)) if len(cls.occurrences(ocel)) > 2 else 0
    @classmethod
    def kurtosis_variant_occurrence(cls, ocel): return stats.kurtosis(cls.occurrences(ocel)) if len(cls.occurrences(ocel)) > 2 else 0

    # Additional variant metrics used in the evaluation of OCEL-Gen
    @classmethod
    def rmc_object(cls, ocel):
        """Ratio of most common variant occurrence to number of objects."""
        occ = cls.occurrences(ocel)
        return occ[0] / len(ocel["ocel:objects"]) if occ else 0

    @classmethod
    def rt10_object(cls, ocel):
        """Ratio of objects in top 10% frequent variants to number od objects."""
        occ = cls.occurrences(ocel)
        cutoff = max(1, int(len(occ) * 0.10))
        return sum(occ[:cutoff]) / len(ocel["ocel:objects"]) if occ else 0

    @classmethod
    def rvpnot_object(cls, ocel):
        """Ratio of unique variants to number of objects."""
        occ = cls.occurrences(ocel)
        return len(occ) / len(ocel["ocel:objects"]) if occ else 0

    def extract(self, ocel):
        """
        Extract the selected variant-based features.

        Args:
            ocel (dict): The OCEL log.

        Returns:
            dict: Selected feature name to value mapping.
        """
        return {
            name: method(ocel)
            for name, method in inspect.getmembers(self.__class__, predicate=inspect.ismethod)
            if name in self.feature_names and name != "occurrences"
        }
