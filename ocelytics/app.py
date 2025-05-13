import streamlit as st
import pandas as pd
import tempfile
from ocelytics.feature_extractor import extract_features

# Page setup
st.set_page_config(page_title="OCELytics", layout="wide")
st.title("📊 OCELytics – OCEL Feature Extraction Tool")

st.sidebar.header("Upload and Select Options")

# File upload
uploaded_file = st.sidebar.file_uploader("Upload OCEL log (.jsonocel)", type=["jsonocel"])

# Feature selection
feature_types = [
    "log_level", 
    "activity_level", 
    "object_level", 
    "path_length", 
    "path_variant"
]
selected_features = st.sidebar.multiselect("Select feature types to extract:", feature_types, default=["log_level"])

if uploaded_file and selected_features:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jsonocel") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.success("File uploaded successfully!")

    with st.spinner("🔍 Extracting features..."):
        try:
            results = extract_features(input_path=tmp_path, feature_types=selected_features)

            if isinstance(results, dict):
                df = pd.DataFrame.from_dict(results, orient='index', columns=["Value"])
                st.subheader("📈 Extracted Features")
                st.dataframe(df)
                csv = df.to_csv().encode('utf-8')
                st.download_button("📥 Download CSV", data=csv, file_name="ocelytics_features.csv", mime="text/csv")
            else:
                st.error("❌ Unexpected result format. Expected a dictionary.")

        except Exception as e:
            st.error(f"🚨 An error occurred: {e}")
else:
    st.info("📂 Please upload a `.jsonocel` file and select feature types.")
