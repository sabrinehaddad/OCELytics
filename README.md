# OCELytics – Feature Extraction from Object-Centric Event Logs

**OCELytics** is a Python toolkit for extracting numerical features from object-centric event logs (OCEL). It allows you to profile process behavior across object types and dimensions using statistical and structural descriptors. These features can be used for log similarity analysis, machine learning, clustering, anomaly detection, and more.

---

## Key Features

- Extract features by:
  - **Feature type** (e.g., `'path_variant'`, `'temporal'`)
  - **Feature name** (e.g., `'n_objects'`, `'path_len_mean'`)
- Optimized for the **OCEL data standard** [[2]](#references
- Extensible via `feature_registry.py`

---

## Installation

### Requirements
- Python 3.9+
- Required dependencies:
```bash
pip install numpy pandas scipy pm4py
```

---

## Full Feature Table

| **Feature Type**       | **Feature Names** |
|------------------------|-------------------|
| `simple_stats`         | `n_objects`, `n_object_variants` |
| `objects`              | `n_objects`, `n_object_types` |
| `activities`           | `n_unique_activities`, `activities_min`, `activities_max`, `activities_mean`, `activities_median`, `activities_std`, `activities_variance`, `activities_q1`, `activities_q3`, `activities_iqr`, `activities_skewness`, `activities_kurtosis` |
| `path_variant`         | `ratio_most_common_variant`, `ratio_top_1_variants`, `ratio_top_5_variants`, `ratio_top_10_variants`, `ratio_top_20_variants`, `ratio_top_50_variants`, `ratio_top_75_variants`, `mean_variant_occurrence`, `std_variant_occurrence`, `skewness_variant_occurrence`, `kurtosis_variant_occurrence`, `rmc_object`, `rt10_object`, `rvpnot_object` |
| `path_length`          | `path_len_min`, `path_len_max`, `path_len_mean`, `path_len_median`, `path_len_mode`, `path_len_std`, `path_len_variance`, `path_len_q1`, `path_len_q3`, `path_len_iqr`, `path_len_geometric_mean`, `path_len_geometric_std`, `path_len_harmonic_mean`, `path_len_skewness`, `path_len_kurtosis`, `path_len_entropy`, `path_len_coefficient_variation`, `path_len_hist1` to `path_len_hist10`, `path_len_skewness_hist`, `path_len_kurtosis_hist` |
| `start_activities`     | `n_unique_start_activities`, `start_activities_min`, `start_activities_max`, `start_activities_mean`, `start_activities_median`, `start_activities_std`, `start_activities_variance`, `start_activities_q1`, `start_activities_q3`, `start_activities_iqr`, `start_activities_skewness`, `start_activities_kurtosis` |
| `end_activities`       | `n_unique_end_activities`, `end_activities_min`, `end_activities_max`, `end_activities_mean`, `end_activities_median`, `end_activities_std`, `end_activities_variance`, `end_activities_q1`, `end_activities_q3`, `end_activities_iqr`, `end_activities_skewness`, `end_activities_kurtosis` |
| `temporal`             | `temporal_duration`, `temporal_avg_time_diff`, `temporal_std_time_diff` |

---

## Usage Examples

For the following examples Order Management event data [[1]](#references).

### Example 1 – Extract by Feature Type

```bash
python -c "from ocelytics.feature_extractor import extract_features; print(extract_features('data/OrderManagement.jsonocel', ['path_length', 'path_variant']))"
```

outputs
```python
SUCCESSFULLY: 43 features for OrderManagement. Took 0:00:01.258468.
{'log': 'OrderManagement', 'path_len_coefficient_variation': 8.274502211175925, 'path_len_entropy': 7.406439183976054, 'path_len_geometric_mean': 8.108081727214321, 'path_len_geometric_std': 1.7371903876364025, 'path_len_harmonic_mean': 7.192398909028824, 'path_len_hist1': 0.003140480381924419, 'path_len_hist10': 3.008122971191971e-06, 'path_len_hist2': 0.0, 'path_len_hist3': 0.0, 'path_len_hist4': 1.9142600725767096e-06, 'path_len_hist5': 2.7346572465381556e-06, 'path_len_hist6': 0.0, 'path_len_hist7': 0.0, 'path_len_hist8': 0.0, 'path_len_hist9': 2.46119152188434e-06, 'path_len_iqr': 2.0, 'path_len_kurtosis': 432.2698269273913, 'path_len_kurtosis_hist': 5.111085025880998, 'path_len_max': 3177, 'path_len_mean': 15.819373318288344, 'path_len_median': 8.0, 'path_len_min': 3, 'path_len_mode': 7, 'path_len_q1': 7.0, 'path_len_q3': 9.0, 'path_len_skewness': 20.343108548712443, 'path_len_skewness_hist': 2.6666582832601624, 'path_len_std': 130.89743950159433, 'path_len_variance': 17134.139668073552, 'kurtosis_variant_occurrence': 357.7702950204135, 'mean_variant_occurrence': 5.740408570004982, 'ratio_most_common_variant': 0.10102412775559799, 'ratio_top_10_variants': 0.8344905398368339, 'ratio_top_1_variants': 0.6085749001909391, 'ratio_top_20_variants': 0.8605276861655963, 'ratio_top_50_variants': 0.9127755597986461, 'ratio_top_5_variants': 0.7970838396111786, 'ratio_top_75_variants': 0.9563443846554418, 'rmc_object': 0.10102412775559799, 'rt10_object': 0.8344905398368339, 'rvpnot_object': 0.17418850893942023, 'skewness_variant_occurrence': 17.679531704397018, 'std_variant_occurrence': 47.55313160343866}
```

### Example 2 – Extract by Feature Name

```bash
python -c "from ocelytics.feature_extractor import extract_features; print(extract_features('data/OrderManagement.jsonocel', ['path_len_entropy', 'ratio_most_common_variant']))"
```

outputs
```python
SUCCESSFULLY: 12 features for OrderManagement. Took 0:00:00.220417.
{'log': 'OrderManagement', 'activities_iqr': 675.0, 'activities_kurtosis': 4.963272072286839, 'activities_max': 8159, 'activities_mean': 2033.3636363636363, 'activities_median': 1664.0, 'activities_min': 391, 'activities_q1': 1325.0, 'activities_q3': 2000.0, 'activities_skewness': 2.4821800661600624, 'activities_std': 2007.0507658899674, 'activities_variance': 4028252.776859504, 'n_unique_activities': 11}
```

### Example 3 – Extract All Features

```bash
python -c "from ocelytics.feature_extractor import extract_features; print(extract_features('data/OrderManagement.jsonocel'))"
```
outputs
```python
SUCCESSFULLY: 58 features for OrderManagement. Took 0:00:01.857049.
{'log': 'OrderManagement', 'path_len_coefficient_variation': 8.274502211175925, 'path_len_entropy': 7.406439183976054, 'path_len_geometric_mean': 8.108081727214321, 'path_len_geometric_std': 1.7371903876364025, 'path_len_harmonic_mean': 7.192398909028824, 'path_len_hist1': 0.003140480381924419, 'path_len_hist10': 3.008122971191971e-06, 'path_len_hist2': 0.0, 'path_len_hist3': 0.0, 'path_len_hist4': 1.9142600725767096e-06, 'path_len_hist5': 2.7346572465381556e-06, 'path_len_hist6': 0.0, 'path_len_hist7': 0.0, 'path_len_hist8': 0.0, 'path_len_hist9': 2.46119152188434e-06, 'path_len_iqr': 2.0, 'path_len_kurtosis': 432.2698269273913, 'path_len_kurtosis_hist': 5.111085025880998, 'path_len_max': 3177, 'path_len_mean': 15.819373318288344, 'path_len_median': 8.0, 'path_len_min': 3, 'path_len_mode': 7, 'path_len_q1': 7.0, 'path_len_q3': 9.0, 'path_len_skewness': 20.343108548712443, 'path_len_skewness_hist': 2.6666582832601624, 'path_len_std': 130.89743950159433, 'path_len_variance': 17134.139668073552, 'n_object_types': 5, 'n_objects': 11522, 'n_object_variants': 1968, 'activities_iqr': 675.0, 'activities_kurtosis': 4.963272072286839, 'activities_max': 8159, 'activities_mean': 2033.3636363636363, 'activities_median': 1664.0, 'activities_min': 391, 'activities_q1': 1325.0, 'activities_q3': 2000.0, 'activities_skewness': 2.4821800661600624, 'activities_std': 2007.0507658899674, 'activities_variance': 4028252.776859504, 'n_unique_activities': 11, 'kurtosis_variant_occurrence': 357.7702950204135, 'mean_variant_occurrence': 5.740408570004982, 'ratio_most_common_variant': 0.10102412775559799, 'ratio_top_10_variants': 0.8344905398368339, 'ratio_top_1_variants': 0.6085749001909391, 'ratio_top_20_variants': 0.8605276861655963, 'ratio_top_50_variants': 0.9127755597986461, 'ratio_top_5_variants': 0.7970838396111786, 'ratio_top_75_variants': 0.9563443846554418, 'rmc_object': 0.10102412775559799, 'rt10_object': 0.8344905398368339, 'rvpnot_object': 0.17418850893942023, 'skewness_variant_occurrence': 17.679531704397018, 'std_variant_occurrence': 47.55313160343866}
```
---

## 🌐 Web App Interface

In addition to programmatic and CLI use, OCELytics offers an intuitive **Streamlit-based web interface** for interactive exploration and feature extraction.

### ✅ How to Launch the Web App

```bash
streamlit run ocelytics/app.py
```

After launching, the app will automatically open in your browser at:

```
http://localhost:8501
```

---

### 🧭 What You Can Do in the Web App

- 📂 Upload an `.jsonocel` event log file
- ✅ Choose feature types or individual feature names
- 🔍 Extract features interactively
- 📊 View results in a scrollable, filterable table
- 📥 Download results as a CSV file

!(WebApp.png)
---

## Feature System Design

Each feature group in OCELytics is implemented as a class inheriting from a base `Feature` class. Feature methods are automatically registered via `feature_registry.py`, enabling dynamic selection at runtime. You can extend OCELytics by adding your own feature type module and linking it in the registry.

---

## Applications

- OCEL logs similarity graphs and feature-based clustering
- Descriptive complexity analysis of object-centric event behavior

---

## 📚 References

1. OCEL Standard: https://www.ocel-standard.org/1.0/
2. Inspiration: [FEEED: Feature Extraction from Event Data](https://github.com/lmu-dbs/feeed)
