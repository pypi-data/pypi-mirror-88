from collections import OrderedDict
from .column import Column
from .index import Index


class Table:

    def __init__(self, name, *, dbi=None, metadata=None):
        self._name = name
        self._dbi = dbi
        self._metadata = metadata
        self._columns = None
        self._indexes = None
        self._primaryIndex = None

    @property
    def name(self):
        return self._name

    @property
    def dbi(self):
        return self._dbi

    @property
    def metadata(self):
        return self._metadata or {}

    @property
    def columns(self):
        if self._columns is None:
            self._columns = self.readColumns()
        return self._columns

    @property
    def indexes(self):
        if self._indexes is None:
            self._indexes = self.readIndexes()
        return self._indexes

    @property
    def primaryIndex(self):
        if self._indexes is None:
            self._indexes = self.readIndexes()
        return self._primaryIndex

    @property
    def tableType(self):
        return self.metadata.get('TABLE_TYPE')

    @property
    def comment(self):
        return self.metadata.get('TABLE_COMMENT')

    def readColumns(self):
        result = OrderedDict()
        if self.dbi and hasattr(self.dbi, 'queryColumns'):
            for column in self.dbi.queryColumns(table=self):
                column._parent = self
                result[column.name] = column
        result.__setitem__ = None
        return result

    def readIndexes(self):
        result = OrderedDict()
        if self.dbi and hasattr(self.dbi, 'queryIndexes'):
            for index in self.dbi.queryIndexes(table=self):
                index._parent = self
                result[index.name] = index
                if index.primary:
                    self._primaryIndex = index
        result.__setitem__ = None
        return result
