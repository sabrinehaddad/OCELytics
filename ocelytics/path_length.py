"""
Computes statistics over the lengths of object-centric paths (number of events per object).
"""

import numpy as np
from scipy import stats
from .feature import Feature

class PathLength(Feature):
    """
    Extracts descriptive statistics based on the number of events per object.
    """

    def __init__(self, feature_names=None):
        self.feature_type = "path_length"
        super().__init__(feature_names)

        self.available_class_methods = {
            fname: getattr(self, fname)
            for fname in dir(self)
            if not fname.startswith("_") and callable(getattr(self, fname)) and fname.startswith("path_len")
        }

    @staticmethod
    def get_path_lengths(log):
        """
        Count the number of events each object participates in.

        Args:
            log (dict): Parsed OCEL log.

        Returns:
            list[int]: Event counts per object.
        """
        object_lengths = {}
        for event in log["ocel:events"].values():
            for obj in event.get("ocel:omap", []):
                object_lengths[obj] = object_lengths.get(obj, 0) + 1
        return list(object_lengths.values())

    # Basic statistics
    @classmethod
    def path_len_min(cls, log): return np.min(cls.get_path_lengths(log))
    @classmethod
    def path_len_max(cls, log): return np.max(cls.get_path_lengths(log))
    @classmethod
    def path_len_mean(cls, log): return np.mean(cls.get_path_lengths(log))
    @classmethod
    def path_len_median(cls, log): return np.median(cls.get_path_lengths(log))
    @classmethod
    def path_len_mode(cls, log): 
        values, counts = np.unique(cls.get_path_lengths(log), return_counts=True)
        return values[np.argmax(counts)]
    @classmethod
    def path_len_std(cls, log): return np.std(cls.get_path_lengths(log))
    @classmethod
    def path_len_variance(cls, log): return np.var(cls.get_path_lengths(log))
    @classmethod
    def path_len_q1(cls, log): return np.percentile(cls.get_path_lengths(log), 25)
    @classmethod
    def path_len_q3(cls, log): return np.percentile(cls.get_path_lengths(log), 75)
    @classmethod
    def path_len_iqr(cls, log): return stats.iqr(cls.get_path_lengths(log))

    # Geometric/harmonic statistics
    @classmethod
    def path_len_geometric_mean(cls, log): return stats.gmean(cls.get_path_lengths(log))
    @classmethod
    def path_len_geometric_std(cls, log): return stats.gstd(cls.get_path_lengths(log))
    @classmethod
    def path_len_harmonic_mean(cls, log): return stats.hmean(cls.get_path_lengths(log))

    # Shape statistics
    @classmethod
    def path_len_skewness(cls, log): return stats.skew(cls.get_path_lengths(log))
    @classmethod
    def path_len_kurtosis(cls, log): return stats.kurtosis(cls.get_path_lengths(log))

    @classmethod
    def path_len_entropy(cls, log):
        """
        Compute entropy of the path length distribution.

        Returns:
            float: Entropy value.
        """
        values = cls.get_path_lengths(log)
        value_counts = np.bincount(values)
        probs = value_counts / np.sum(value_counts)
        return -np.sum(probs[probs > 0] * np.log2(probs[probs > 0]))

    @classmethod
    def path_len_coefficient_variation(cls, log):
        """
        Compute coefficient of variation: std / mean.

        Returns:
            float: Coefficient of variation.
        """
        values = cls.get_path_lengths(log)
        return np.std(values) / np.mean(values)

    @classmethod
    def path_len_skewness_hist(cls, log):
        """
        Skewness of histogram bin values from the distribution.
        """
        hist = np.histogram(cls.get_path_lengths(log), bins=10, density=True)[0]
        return stats.skew(hist)

    @classmethod
    def path_len_kurtosis_hist(cls, log):
        """
        Kurtosis of histogram bin values from the distribution.
        """
        hist = np.histogram(cls.get_path_lengths(log), bins=10, density=True)[0]
        return stats.kurtosis(hist)


    @classmethod
    def path_len_hist1(cls, log): return np.histogram(cls.get_path_lengths(log), bins=10, density=True)[0][0]
    @classmethod
    def path_len_hist2(cls, log): return np.histogram(cls.get_path_lengths(log), bins=10, density=True)[0][1]
    @classmethod
    def path_len_hist3(cls, log): return np.histogram(cls.get_path_lengths(log), bins=10, density=True)[0][2]
    @classmethod
    def path_len_hist4(cls, log): return np.histogram(cls.get_path_lengths(log), bins=10, density=True)[0][3]
    @classmethod
    def path_len_hist5(cls, log): return np.histogram(cls.get_path_lengths(log), bins=10, density=True)[0][4]
    @classmethod
    def path_len_hist6(cls, log): return np.histogram(cls.get_path_lengths(log), bins=10, density=True)[0][5]
    @classmethod
    def path_len_hist7(cls, log): return np.histogram(cls.get_path_lengths(log), bins=10, density=True)[0][6]
    @classmethod
    def path_len_hist8(cls, log): return np.histogram(cls.get_path_lengths(log), bins=10, density=True)[0][7]
    @classmethod
    def path_len_hist9(cls, log): return np.histogram(cls.get_path_lengths(log), bins=10, density=True)[0][8]
    @classmethod
    def path_len_hist10(cls, log): return np.histogram(cls.get_path_lengths(log), bins=10, density=True)[0][9]
