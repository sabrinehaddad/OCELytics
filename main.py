from datetime import datetime as dt
from ocelytics.feature_extractor import extract_features
import json
import numpy as np
import sys

def default_handler(obj):
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    elif isinstance(obj, np.integer):
        return int(obj)
    else:
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

if __name__ == '__main__':
    LOG_PATH = "test_data/sample_log.jsonocel"
    AVAILABLE_FEATURE_TYPES = [
        "activity_level",
        "object_level",
        "log_level",
        "path_length",
        "path_variant"
    ]

    print("📊 Available feature types:")
    for i, ft in enumerate(AVAILABLE_FEATURE_TYPES, 1):
        print(f"  {i}. {ft}")

    selected_type = input("🧠 Enter the feature type you want to extract: ").strip().lower()

    if selected_type not in AVAILABLE_FEATURE_TYPES:
        print(f"❌ Invalid feature type: '{selected_type}'. Must be one of: {', '.join(AVAILABLE_FEATURE_TYPES)}")
        sys.exit(1)

    start_time = dt.now()
    print(f"\n🚀 Extracting '{selected_type}' features from: {LOG_PATH}")

    features = extract_features(LOG_PATH, feature_types=[selected_type])

    print(f"\n✅ Extracted features for '{selected_type}':")
    for key, val in features.items():
        if key != "log":
            print(f"  {key}: {val}")

    with open("output.json", "w") as f:
        json.dump(features, f, indent=2, default=default_handler)

    print(f"\n✅ Finished in {dt.now() - start_time}. Output saved to output.json")