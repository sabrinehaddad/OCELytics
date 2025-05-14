import inspect
import numpy as np
from scipy import stats
from .feature import Feature

class PathLength(Feature):
    def __init__(self, feature_names='path_length'):
        self.feature_type = "path_length"
        self.available_class_methods = dict(inspect.getmembers(PathLength, predicate=inspect.ismethod))
        if self.feature_type in feature_names:
            self.feature_names = [*self.available_class_methods.keys()]
        else:
            self.feature_names = feature_names

    @staticmethod
    def object_path_lengths(log):
        object_events = {}
        for event_id, event in log["ocel:events"].items():
            for obj_id in event.get("ocel:omap", []):
                object_events.setdefault(obj_id, []).append(event_id)
        return [len(events) for events in object_events.values()]

    @staticmethod
    def path_len_hist(log):
        path_lengths = PathLength.object_path_lengths(log)
        result, _ = np.histogram(path_lengths, bins=10, density=True)
        return result

    @classmethod
    def path_len_min(cls, log): return np.min(cls.object_path_lengths(log))
    @classmethod
    def path_len_max(cls, log): return np.max(cls.object_path_lengths(log))
    @classmethod
    def path_len_mean(cls, log): return np.mean(cls.object_path_lengths(log))
    @classmethod
    def path_len_median(cls, log): return np.median(cls.object_path_lengths(log))
    @classmethod
    def path_len_mode(cls, log): return stats.mode(cls.object_path_lengths(log), keepdims=False)[0]
    @classmethod
    def path_len_std(cls, log): return np.std(cls.object_path_lengths(log))
    @classmethod
    def path_len_variance(cls, log): return np.var(cls.object_path_lengths(log))
    @classmethod
    def path_len_q1(cls, log): return np.percentile(cls.object_path_lengths(log), 25)
    @classmethod
    def path_len_q3(cls, log): return np.percentile(cls.object_path_lengths(log), 75)
    @classmethod
    def path_len_iqr(cls, log): return stats.iqr(cls.object_path_lengths(log))
    @classmethod
    def path_len_geometric_mean(cls, log): return stats.gmean(cls.object_path_lengths(log))
    @classmethod
    def path_len_geometric_std(cls, log): return stats.gstd(cls.object_path_lengths(log))
    @classmethod
    def path_len_harmonic_mean(cls, log): return stats.hmean(cls.object_path_lengths(log))
    @classmethod
    def path_len_skewness(cls, log): return stats.skew(cls.object_path_lengths(log))
    @classmethod
    def path_len_kurtosis(cls, log): return stats.kurtosis(cls.object_path_lengths(log))
    @classmethod
    def path_len_coefficient_variation(cls, log): return stats.variation(cls.object_path_lengths(log))
    @classmethod
    def path_len_entropy(cls, log): return stats.entropy(cls.object_path_lengths(log))

    # Histogram bins
    @classmethod
    def path_len_hist1(cls, log): return cls.path_len_hist(log)[0]
    @classmethod
    def path_len_hist2(cls, log): return cls.path_len_hist(log)[1]
    @classmethod
    def path_len_hist3(cls, log): return cls.path_len_hist(log)[2]
    @classmethod
    def path_len_hist4(cls, log): return cls.path_len_hist(log)[3]
    @classmethod
    def path_len_hist5(cls, log): return cls.path_len_hist(log)[4]
    @classmethod
    def path_len_hist6(cls, log): return cls.path_len_hist(log)[5]
    @classmethod
    def path_len_hist7(cls, log): return cls.path_len_hist(log)[6]
    @classmethod
    def path_len_hist8(cls, log): return cls.path_len_hist(log)[7]
    @classmethod
    def path_len_hist9(cls, log): return cls.path_len_hist(log)[8]
    @classmethod
    def path_len_hist10(cls, log): return cls.path_len_hist(log)[9]

    @classmethod
    def path_len_skewness_hist(cls, log): return stats.skew(cls.path_len_hist(log))
    @classmethod
    def path_len_kurtosis_hist(cls, log): return stats.kurtosis(cls.path_len_hist(log))

    def extract(self, log):
        return {
            name: method(log)
            for name, method in inspect.getmembers(self.__class__, predicate=inspect.ismethod)
            if name in self.feature_names
        }

# Entry point for CLI or batch extractor
def extract(log):
    return PathLength().extract(log)
