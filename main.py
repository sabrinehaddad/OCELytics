from ocelytics.feature_extractor import extract_features

features = extract_features("test_data/sample_log.jsonocel", feature_types=["path_variant"])

print(features)