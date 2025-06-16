import inspect

class Feature:
    """
    Base class for defining OCEL-based feature extractors.
    """

    def __init__(self, feature_names=None):
        """
        Initialize the feature extractor and select which features to compute.

        Args:
            feature_names (list[str], optional): Names of features to compute. 
                If None, all available features are used.
        """
        self.feature_type = getattr(self, 'feature_type', None)
        self.available_class_methods = {
            name: method
            for name, method in inspect.getmembers(self.__class__, predicate=inspect.ismethod)
        }

        if feature_names is None or self.feature_type in feature_names:
            self.feature_names = list(self.available_class_methods.keys())
        else:
            self.feature_names = feature_names

    def extract(self, log):
        """
        Run feature methods on the provided OCEL log.

        Args:
            log (dict): Parsed OCEL log.

        Returns:
            dict: Feature name to value mapping.
        """
        output = {}
        for name in self.feature_names:
            fn = self.available_class_methods[name]
            output[name] = fn(log)
        return output
