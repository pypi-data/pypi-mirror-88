
from .column import Column


class Index:

    def __init__(self, columns, *, name=None, table=None, metadata=None):
        self._name = name
        self._table = table
        self._columns = columns
        self._metadata = metadata

    @property
    def name(self):
        return self._name

    @property
    def columns(self):
        return self._columns

    @property
    def primary(self):
        return None

    @property
    def unique(self):
        return None

    @property
    def table(self):
        return self._table

    @property
    def metadata(self):
        return self._metadata or {}

    def __getattr__(self, name):
        if self._metadata is None or name not in self._metadata:
            raise AttributeError('no metadata available')
        return self._metadata[name]
