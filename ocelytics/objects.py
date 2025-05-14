import inspect
import numpy as np
from collections import Counter
from .feature import Feature


class Objects(Feature):
    def __init__(self, feature_names=None):
        self.feature_type = "objects"
        self.available_class_methods = dict(inspect.getmembers(self.__class__, predicate=inspect.ismethod))

        if feature_names is None or self.feature_type in feature_names:
            self.feature_names = list(self.available_class_methods.keys())
        else:
            self.feature_names = feature_names

    @staticmethod
    def objects(ocel):
        return ocel.objects

    @staticmethod
    def events(ocel):
        return ocel.events

    @classmethod
    def n_objects(cls, ocel):
        return len(cls.objects(ocel))

    @classmethod
    def n_unique_object_types(cls, ocel):
        return cls.objects(ocel)["ocel:type"].nunique()



    def extract(self, ocel):
        return {
            name: method(ocel)
            for name, method in inspect.getmembers(self.__class__, predicate=inspect.ismethod)
            if name in self.feature_names
        }

