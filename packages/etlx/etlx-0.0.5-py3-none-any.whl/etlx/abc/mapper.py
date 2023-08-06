from collections import OrderedDict
from datetime import datetime
from etlx.abc import RowDict


class RowMapper(OrderedDict):

    def __call__(self, row):
        # result = map(lambda x: x(row), self.values())
        return RowDict((k, f(row)) for k, f in self.items())


class ExtractAttr:

    def __init__(self, key):
        self.key = key

    def __call__(self, row):
        return getattr(row, self.key, None)


class ExtractItem:

    def __init__(self, key):
        self.key = key

    def __call__(self, row):
        return row.get(self.key, None)


class ExtractConst:

    def __init__(self, value):
        self.value = value

    def __call__(self, row):
        return self.value


class Datetime:

    def __init__(self, extractor):
        self.extractor = extractor

    def __call__(self, row):
        value = self.extractor(row)
        if isinstance(value, str):
            value = value.split('.')[0]
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return value
