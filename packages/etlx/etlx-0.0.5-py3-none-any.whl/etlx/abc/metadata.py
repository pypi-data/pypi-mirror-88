from typing import Mapping
from collections import OrderedDict
from .table import Table, Column, Index


class MetadataMixIn:

    METADATA_LAZY_READ = True

    Table = Table

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tables = None
        self._tablesLazyRead = self.METADATA_LAZY_READ

    @property
    def tables(self) -> Mapping[str, Table]:
        if self._tables is None:
            self.loadTables()
        return self._tables

    def __call__(self, name) -> Table:
        return self.tables[name]

    def loadTables(self):
        self._tables = self.readTables(lazyRead=self._tablesLazyRead)

    def readTables(self, *, lazyRead=True):
        tables = OrderedDict()
        # all TABLES
        for table in self.queryTables():
            tables[table.name] = table
        tables.__setitem__ = None
        if lazyRead:
            return tables
        # init columns & indexes dicts
        for table in tables.values():
            table._columns = OrderedDict()
            table._indexes = OrderedDict()
        # all COLUMNS
        for column in self.queryColumns():
            table = tables[column.table]
            column._parent = table
            table._columns[column.name] = column
        # all INDEXES
        for index in self.queryIndexes():
            table = tables[index.table]
            index._parent = table
            table._indexes[index.name] = index
            if index.primary:
                table._primaryIndex = index
        # make immutable
        for table in tables.values():
            table._columns.__setitem__ = None
            table._indexes.__setitem__ = None
        return tables

    def queryColumns(self, *, table=None, TABLE_CATALOG=None, TABLE_SCHEMA=None):
        if isinstance(table, Table):
            table = table.name
        kwargs = dict(TABLE_NAME=table, TABLE_CATALOG=TABLE_CATALOG, TABLE_SCHEMA=TABLE_SCHEMA)
        sql = "SELECT * FROM information_schema.COLUMNS"
        sql += self._whereFilter(**kwargs)
        sql += " ORDER BY TABLE_NAME, ORDINAL_POSITION"
        result = []
        for row in self.queryAll(sql, **kwargs):
            row = self._rowUpperColumnNames(row)
            tableName = row['TABLE_NAME']
            columnName = row['COLUMN_NAME']
            column = self.Column(name=columnName, table=tableName, metadata=row)
            result.append(column)
        return result

#    def queryIndexes(self, table=None, TABLE_CATALOG=None, TABLE_SCHEMA=None):
#        return []
