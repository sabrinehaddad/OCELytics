import argparse
from ocelytics.feature_extractor import extract_features

def main():
    AVAILABLE_FEATURE_TYPES = [
        "log_level",
        "activity_level",
        "object_level",
        "path_length",
        "path_variant"
    ]

    parser = argparse.ArgumentParser(
        description="📊 OCELytics - Feature extraction for OCEL logs"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to OCEL input file (.jsonocel)"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Path to output CSV file (optional)"
    )
    parser.add_argument(
        "--features", "-f",
        default="all",
        help="Comma-separated list of feature types (e.g., log_level,activity_level). Use 'all' for everything."
    )

    args = parser.parse_args()

    if args.features.strip().lower() == "all":
        feature_types = ["all"]
    else:
        feature_types = [ft.strip() for ft in args.features.split(",")]
        for ft in feature_types:
            if ft not in AVAILABLE_FEATURE_TYPES:
                print(f"❌ Invalid feature type: '{ft}'. Must be one of: {', '.join(AVAILABLE_FEATURE_TYPES)}")
                return

    print(f"\n🚀 Extracting features: {feature_types}")
    print(f"📂 Input file: {args.input}")
    if args.output:
        print(f"💾 Output will be saved to: {args.output}")

    features = extract_features(args.input, args.output, feature_types)

    print("\n✅ Extracted Features:")
    for key, value in features.items():
        print(f"  - {key}: {value}")

if __name__ == "__main__":
    main()
