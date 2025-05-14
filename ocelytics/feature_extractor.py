import json
import pandas as pd
import subprocess
from .activities import Activities as activities
from .simple_stats import SimpleStats as simple_stats
from .path_variant import PathVariant as path_variant
from .path_length import PathLength as path_length
from .objects import Objects as objects
from datetime import datetime as dt

import pm4py

FEATURE_TYPES = [
    "activities",
    "simple_stats",
    "objects",
    "path_variant",
    "path_length"
    ]

def feature_type(feature_name):
    available_features = []
    for feature_type in FEATURE_TYPES:
        available_features.extend([*eval(feature_type)().available_class_methods])
        available_features.append(str(feature_type))
        if feature_name in available_features:
            return feature_type
    raise ValueError(f"ERROR: Invalid value for feature_key argument: {feature_name}. See README.md for " +
                     f"supported feature_names or use a sublist of the following: {FEATURE_TYPES} or None")


def extract_features(event_logs_path, feature_types=None):
    log_name = event_logs_path.rsplit("/", 1)[-1]
    with open(event_logs_path, "r") as f:
      log = json.load(f)

    if feature_types is None:
        feature_types = FEATURE_TYPES
    
    features = {"log": log_name.split(".jsonocel")[0]}
    start_log = dt.now()
    
    for i, ft_name in enumerate(feature_types):
        start_feat = dt.now()
        
        ft_type = feature_type(ft_name)
    
        feature_values = eval(f"{ft_type}(feature_names=['{ft_name}']).extract(log)")
        features = {**features, **feature_values}

        log_info =  f"     INFO: {log_name} starting at {len(features)}, {ft_name} from {ft_type} took {dt.now()-start_feat} sec, "
        if i == len(feature_types) - 1:
            print(log_info + "last feature.")
        else:
            print(log_info + f"next {feature_types[(i+1)%len(feature_types)]}...")
    print(
        f"SUCCESSFULLY: {len(features)-1} features for {log_name} took {dt.now() - start_log} sec."
    )

    return features
