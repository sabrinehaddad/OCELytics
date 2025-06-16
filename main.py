"""
Command-line entry point for OCELytics.

Allows users to extract features from an OCEL log by specifying a file path and
optional feature types or names.

Usage:
    python main.py path/to/log.jsonocel --by activities --out output.json
"""

import argparse
import json
from datetime import datetime as dt

from ocelytics.feature_extractor import extract_features

def main():
    """
    Parse CLI arguments and extract features from an OCEL log.
    """
    parser = argparse.ArgumentParser(description="OCELytics - Feature Extraction from OCEL logs.")
    parser.add_argument("log_path", help="Path to the .jsonocel log file")
    parser.add_argument("--by", nargs="*", default=None, help="List of feature names or types to extract")
    parser.add_argument("--out", default=None, help="Optional output path to save extracted features as JSON")

    args = parser.parse_args()

    print(f"Loading log: {args.log_path}")
    print(f"⚙️ Extracting features (by: {args.by if args.by else 'all'})")

    start = dt.now()
    try:
        features = extract_features(args.log_path, by=args.by)
        print(f"Done in {dt.now() - start}. Extracted {len(features) - 1} features.")
    except Exception as e:
        print(f"Error during extraction: {e}")
        return

    print(json.dumps(features, indent=2))

    if args.out:
        with open(args.out, "w") as f:
            json.dump(features, f, indent=2)
        print(f"Saved to {args.out}")

if __name__ == "__main__":
    main()
