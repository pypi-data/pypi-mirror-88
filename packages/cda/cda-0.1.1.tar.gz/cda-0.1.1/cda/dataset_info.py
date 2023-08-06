from .college_scorecard import MetaData


class DatasetInfo:

    def __init__(self, path):
        self._data = MetaData(path)

    def get_attribute_names(self):
        return self._data.get_attribute_names()
