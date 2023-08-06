from io import StringIO
from decimal import Decimal
from datetime import datetime, date, time


class SQL:
    def __init__(self, dbi=None):
        self.dbi = dbi
        self.buffer = StringIO()

    def __len__(self):
        return self.buffer.tell()

    def __str__(self):
        return self.buffer.getvalue()

    def __bool__(self):
        return len(self) > 0

    def execute(self, *args, **kwargs):
        return self.dbi.execute(self, *args, **kwargs)

    def query(self, *args, **kwargs):
        return self.dbi.query(self, *args, **kwargs)

    def sql(self, sql):
        self.buffer.write(sql)
        return self

    def quoted(self, *args):
        for i, name in enumerate(args):
            self.sql(',' if i else '')
            self.sql('`'+name.replace('`', '``') + '`')
        return self

    def arg(self):
        return self.sql('%s')

    def kwarg(self, name):
        return self.sql(f'%({name})s')

    def literal(self, *args):
        for i, value in enumerate(args):
            self.sql(',' if i else '')
            if value is None:
                self.sql('NULL')
            elif isinstance(value, bool):
                self.sql('1' if value else '0')
            elif isinstance(value, (int, float, Decimal)):
                self.sql(str(value))
            elif isinstance(value, (datetime, date, time)):
                self.sql("'").sql(str(value)).sql("'")
            elif isinstance(value, str):
                value = value.replace("'", "''")
                value = value.replace("%", "%%")
                self.sql("'").sql(value).sql("'")
            elif isinstance(value, tuple):
                self.sql("(").literal(*value).sql(")")
            else:
                raise NotImplementedError()
        return self

    def _list(self, func, iterable, separator=','):
        for i, x in enumerate(iterable):
            self.sql(separator if i else '')
            func(x)

    def SELECT(self, *args):
        self.sql('SELECT ')
        if not args:
            self.sql('* ')
        else:
            self._list(self.quoted, args)
            self.sql(' ')
        return self

    def FROM(self, table):
        self.sql('FROM ')
        self.quoted(table)
        self.sql(' ')
        return self

    def WHERE(self, **kwargs):
        self.sql(' WHERE ')
        for i, (k, v) in enumerate(kwargs.items()):
            self.sql(' AND ' if i else '')
            self.quoted(k).sql('=').literal(v)
        return self

    def _indexInSet(self, index, keys):
        self.sql('(')
        self._list(self.quoted, index)
        self.sql(') IN (')
        self._list(self.literal, keys)
        self.sql(') ')

    def WHERE_INDEX_IN(self, index, keys):
        self.sql('WHERE ')
        self._indexInSet(index, keys)
        return self

    def WHERE_INDEX_KEY(self, index, key):
        self.sql(' WHERE (')
        self._list(self.quoted, index)
        self.sql(')=(')
        self.literal(key)
        self.sql(') ')
        return self

    def INSERT(self, table, **kwargs):
        self.sql('INSERT INTO ').quoted(table)
        self.sql(' (').quoted(*kwargs.keys()).sql(') VALUES (').literal(*kwargs.values()).sql(')')
        return self

    def INSERT_CV(self, table, columns, values):
        self.sql('INSERT INTO ').quoted(table)
        self.sql(' (').quoted(*columns).sql(') VALUES (').literal(*values).sql(')')
        return self

    def UPDATE(self, table, **kwargs):
        self.sql('UPDATE ').quoted(table).sql(' SET ')
        for i, (k, v) in enumerate(kwargs.items()):
            self.sql(',' if i else '')
            self.quoted(k).sql('=').literal(v)
        return self

    def UPDATE_CV(self, table, columns, values):
        self.sql('UPDATE ').quoted(table).sql(' SET ')
        for i, (k, v) in enumerate(zip(columns, values)):
            self.sql(',' if i else '')
            self.quoted(k).sql('=').literal(v)
        return self

    def DELETE(self, table):
        self.sql('DELETE FROM ').quoted(table).sql(' ')
        return self
