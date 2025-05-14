import os

def feature_names():
    with open(f"{os.getcwd()}/ocelytics/utils/column_names.txt") as f:
        columns = f.readlines()
    return [x.strip() for x in columns]