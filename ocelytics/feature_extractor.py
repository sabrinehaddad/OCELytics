import json
from datetime import datetime as dt
from .feature_registry import FEATURE_CLASSES, FEATURE_METHODS

def extract_features(event_logs_input, by=None):
    """
    Extract features from an OCEL log using selected feature classes or method names.

    Args:
        event_logs_input (str or dict): Path to a .jsonocel file or a loaded OCEL log dictionary.
        by (list[str], optional): List of feature types or method names to extract.
                                  If None, all available features are extracted.

    Returns:
        dict: Dictionary mapping feature names to their computed values.
    """
    

    if isinstance(event_logs_input, dict):
        log = event_logs_input
        log_name = "in-memory-log"
    elif isinstance(event_logs_input, str):
        log_name = event_logs_input.rsplit("/", 1)[-1].replace(".jsonocel", "")
        with open(event_logs_input, "r") as f:
            log = json.load(f)
    else:
        raise ValueError("Invalid input: expected a dict or a file path.")

    start_log = dt.now()
    features = {"log": log_name}

    if by is None:
        by = list(FEATURE_CLASSES.keys())

    # Separate selected types and method names
    selected_types = set()
    selected_names = []

    for entry in by:
        if entry in FEATURE_CLASSES:
            selected_types.add(entry)
        elif entry in FEATURE_METHODS:
            selected_names.append(entry)
        else:
            raise ValueError(f"Unknown feature type or name: {entry}")

    # Extract by type
    for ftype in selected_types:
        cls = FEATURE_CLASSES[ftype]
        instance = cls()
        features.update(instance.extract(log))

    # Extract by name
    grouped = {}
    for fname in selected_names:
        ftype = FEATURE_METHODS[fname]
        grouped.setdefault(ftype, []).append(fname)

    for ftype, fnames in grouped.items():
        cls = FEATURE_CLASSES[ftype]
        instance = cls(feature_names=fnames)
        features.update(instance.extract(log))

    print(f"SUCCESSFULLY: {len(features) - 1} features for {log_name}. Took {dt.now() - start_log}.")
    return features
