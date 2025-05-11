import inspect
from .feature import Feature

class LogLevel(Feature):
    def __init__(self):
        super().__init__()
        self.feature_names = [
            "n_events",
            "n_objects",
            "n_object_types",
            "n_activities"
        ]

    @staticmethod
    def events(ocel):
        return ocel.get("ocel:events", {})

    @staticmethod
    def objects(ocel):
        return ocel.get("ocel:objects", {})

    @classmethod
    def n_events(cls, ocel):
        return len(cls.events(ocel))

    @classmethod
    def n_objects(cls, ocel):
        return len(cls.objects(ocel))

    @classmethod
    def n_object_types(cls, ocel):
        object_types = {obj.get("ocel:type") for obj in cls.objects(ocel).values()}
        return len(object_types)

    @classmethod
    def n_activities(cls, ocel):
        activities = {event.get("ocel:activity") for event in cls.events(ocel).values()}
        return len(activities)

    def extract(self, ocel):
        return {
            name: method(ocel)
            for name, method in inspect.getmembers(self.__class__, predicate=inspect.ismethod)
            if name in self.feature_names
        }


def extract(log):
    return LogLevel().extract(log)
