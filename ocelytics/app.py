"""
Streamlit app for OCELytics.

Allows users to upload OCEL log files, select features to extract,
view results in a table, and download them as CSV.
"""

import sys
import os
import streamlit as st
import pandas as pd
import tempfile

# Ensure module path includes the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ocelytics.feature_extractor import extract_features
from ocelytics.feature_registry import FEATURE_CLASSES, FEATURE_METHODS

# App configuration
st.set_page_config(page_title="OCELytics", layout="wide")
st.title("OCELytics – Extracting Features from OCEL logs")
st.sidebar.header("Upload and Select Options")

# Upload OCEL file
uploaded_file = st.sidebar.file_uploader("Upload OCEL log (.jsonocel)", type=["jsonocel"])

# Feature selection
all_feature_types = list(FEATURE_CLASSES.keys())
all_feature_names = list(FEATURE_METHODS.keys())

st.sidebar.subheader("Feature Selection")
selection_mode = st.sidebar.radio("Select features by:", ["Type", "Individual Feature", "All"])
selected_features = []

if selection_mode == "Type":
    selected_features = st.sidebar.multiselect("Choose feature types:", all_feature_types, default=all_feature_types)
elif selection_mode == "Individual Feature":
    selected_features = st.sidebar.multiselect("Choose specific features:", all_feature_names)
elif selection_mode == "All":
    selected_features = None

# Run extraction if inputs are provided
if uploaded_file and (selected_features or selected_features is None):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jsonocel") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.success(" File uploaded successfully!")

    with st.spinner(" Extracting features..."):
        try:
            results = extract_features(event_logs_input=tmp_path, by=selected_features)

            if isinstance(results, dict):
                df = pd.DataFrame.from_dict(results, orient="index", columns=["Value"])
                st.subheader("📈 Extracted Features")

                with st.expander("Click to show all extracted features", expanded=True):
                    num_rows = df.shape[0]
                    row_height = 35
                    max_height = 1000
                    calculated_height = min(row_height * (num_rows + 1), max_height)

                st.dataframe(df, use_container_width=True, height=calculated_height)

                csv = df.to_csv().encode("utf-8")
                st.download_button("📥 Download CSV", data=csv, file_name="ocelytics_features.csv", mime="text/csv")
            else:
                st.error(" Unexpected result format. Expected a dictionary.")
        except Exception as e:
            st.error(f" An error occurred:\n\n{e}")
else:
    st.info("Please upload a `.jsonocel` file and select feature types or names.")
