"""
Feature registry for OCELytics.

Defines available feature classes and maps each individual feature method name
to its corresponding feature type.
"""

from .activities import Activities
from .simple_stats import SimpleStats
from .path_variant import PathVariant
from .path_length import PathLength
from .objects import Objects
from .temporal import Temporal
from .start_activities import StartActivities
from .end_activities import EndActivities


FEATURE_CLASSES = {
    "activities": Activities,
    "simple_stats": SimpleStats,
    "objects": Objects,
    "path_variant": PathVariant,
    "path_length": PathLength,
    "temporal": Temporal,
    "start_activities": StartActivities,
    "end_activities": EndActivities
}

FEATURE_METHODS = {}


for ftype_name, cls in FEATURE_CLASSES.items():
    instance = cls()
    for fname in instance.available_class_methods.keys():
        FEATURE_METHODS[fname] = ftype_name
