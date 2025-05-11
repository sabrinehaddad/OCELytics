class Feature:
    def __init__(self, feature_names=None):
        """
        Initialize the feature extractor.

        :param feature_names: list of feature names to extract. If None, extract all available.
        """
        self.feature_names = feature_names

    def extract(self, log):
        """
        Extract the selected features from the given log.

        :param log: OCEL log (dict format)
        :return: dict of extracted features
        """
        feature_names = self.feature_names

        # Default: extract all available features
        if feature_names is None:
            feature_names = list(self.available_class_methods.keys())

        output = {}
        for feature_name in feature_names:
            if feature_name not in self.available_class_methods:
                raise ValueError(f"❌ Feature '{feature_name}' is not available.")
            feature_fn = self.available_class_methods[feature_name]
            feature_value = feature_fn(log)
            output[feature_name] = feature_value

        return output
