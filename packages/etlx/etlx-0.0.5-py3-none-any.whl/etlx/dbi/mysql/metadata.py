from collections import OrderedDict
from itertools import groupby
from etlx.abc import Column, Index, MetadataMixIn, Table


class MySQL_Table(Table):

    @property
    def database(self):
        return self.metadata.get('TABLE_SCHEMA')


class MySQL_Column(Column):

    @property
    def database(self):
        return self.metadata.get('TABLE_SCHEMA')


class MySQL_Index(Index):

    @property
    def database(self):
        return self.metadata.get('TABLE_SCHEMA')

    @property
    def primary(self):
        return self.name == 'PRIMARY'

    @property
    def unique(self):
        return self.metadata.get('NON_UNIQUE') == 0


class MySQL_MetadataMixIn(MetadataMixIn):

    Table = MySQL_Table
    Column = MySQL_Column
    Index = MySQL_Index

    def queryTables(self, database=None):
        sql = "SELECT * FROM information_schema.TABLES WHERE"
        if database:
            sql += f" TABLE_SCHEMA='{database}'"
        else:
            sql += " TABLE_SCHEMA=DATABASE()"
        sql += " ORDER BY TABLE_NAME"
        result = []
        for row in self.query(sql):
            tableName = row['TABLE_NAME']
            table = self.Table(name=tableName, dbi=self, metadata=row)
            result.append(table)
        return result

    def queryColumns(self, *, table=None, database=None):
        sql = "SELECT * FROM information_schema.COLUMNS WHERE "
        if table is not None:
            sql += f" TABLE_NAME='{table.name}' AND TABLE_SCHEMA='{table.database}'"
        sql += " ORDER BY TABLE_NAME, ORDINAL_POSITION"
        result = []
        for row in self.query(sql):
            tableName = row['TABLE_NAME']
            columnName = row['COLUMN_NAME']
            column = self.Column(name=columnName, table=tableName, metadata=row)
            result.append(column)
        return result

    def queryIndexes(self, *, table=None, database=None):
        sql = "SELECT * FROM information_schema.STATISTICS WHERE"
        if table is not None:
            sql += f" TABLE_NAME='{table.name}' AND TABLE_SCHEMA='{table.database}' AND INDEX_SCHEMA='{table.database}'"
        sql += " ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX"
        result = []
        iterable = self.query(sql)
        groupKey = lambda x: (x['TABLE_NAME'], x['INDEX_NAME'])
        for (TABLE_NAME, INDEX_NAME), group in groupby(iterable, groupKey):
            idxRow = None
            columns = OrderedDict()
            for row in group:
                if idxRow is None:
                    keys = ('TABLE_SCHEMA', 'TABLE_NAME', 'INDEX_NAME', 'NON_UNIQUE', 'INDEX_TYPE', 'INDEX_COMMENT')
                    idxRow = OrderedDict((k, row.get(k)) for k in keys)
                COLUMN_NAME = row['COLUMN_NAME']
                columns[COLUMN_NAME] = row
            columns.__setitem__ = None
            index = self.Index(name=INDEX_NAME, columns=columns, table=TABLE_NAME, metadata=idxRow)
            result.append(index)
        return result
