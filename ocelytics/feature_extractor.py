import json
import pandas as pd

def extract_features(input_path, output_path=None, feature_types=["all"]):
    """
    Extract features from an OCEL log and return them as a dictionary.
    Optionally saves the result to a CSV file if output_path is provided.
    """
    with open(input_path, 'r') as f:
        log = json.load(f)

    features = {}

    if "all" in feature_types or "log_level" in feature_types:
        try:
            from . import simple_stats
            features.update(simple_stats.extract(log))
        except Exception as e:
            print("❌ Failed to extract log_level features:", e)

    if "activity_level" in feature_types:
        try:
            from . import activities
            features.update(activities.extract(log))
        except Exception as e:
            print("❌ Failed to extract activity_level features:", e)

    if "object_level" in feature_types:
        try:
            from . import object_level
            features.update(object_level.extract(log))
        except Exception as e:
            print("❌ Failed to extract object_level features:", e)

    if "path_length" in feature_types:
        try:
            from . import path_length
            features.update(path_length.extract(log))
        except Exception as e:
            print("❌ Failed to extract path_length features:", e)

    if "path_variant" in feature_types:
        try:
            from . import path_variant
            features.update(path_variant.extract(log))
        except Exception as e:
            print("❌ Failed to extract path_variant features:", e)

    if output_path:
        df = pd.DataFrame([features])
        df.to_csv(output_path, index=False)
        print(f"\n📁 Features saved to: {output_path}")

    return features

