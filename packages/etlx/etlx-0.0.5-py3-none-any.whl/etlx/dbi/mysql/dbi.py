import MySQLdb
from etlx.abc.row import RowDict


class MySQL_DBI_MySQLdb:

    def __init__(self, *, connect):
        self._connect_kwargs = dict()
        self._connect_kwargs.update(connect)
        self._dbapi = None
        self._close_on_exit = False

    @property
    def database(self):
        return self._connect_kwargs.get('database')

    @property
    def connected(self):
        return self._dbapi is not None

    def connect(self, **kwargs):
        params = dict()
        params.update(self._connect_kwargs)
        params.update(kwargs)
        params = filter(lambda x: bool(x[1]), params.items())
        params = dict(params)
        self._dbapi = MySQLdb.connect(**params)

    def close(self):
        if self._dbapi:
            self._dbapi.close()
            self._dbapi = None

    def commit(self):
        self._dbapi.commit()

    def rollback(self):
        if self._dbapi:
            self._dbapi.rollback()

    def cursor(self, sql, *args, **kwargs):
        if not isinstance(sql, str):
            sql = str(sql)
        cursor = self._dbapi.cursor(cursorclass=MySQLdb.cursors.SSCursor)
        try:
            cursor.execute(sql, args or kwargs)
        except Exception:
            cursor.close()
            raise
        return cursor

    def execute(self, sql, *args, **kwargs):
        with self.cursor(sql, *args, **kwargs) as cursor:
            return cursor.lastrowid

    def query(self, sql, *args, **kwargs):
        with self.cursor(sql, *args, **kwargs) as cursor:
            for row in cursor:
                yield RowDict((d[0], v) for d, v in zip(cursor.description, row))

    def readone(self, sql, *args, **kwargs):
        with self.cursor(sql, *args, **kwargs) as cursor:
            row = cursor.fetchone()
            if row:
                row = RowDict((d[0], v) for d, v in zip(cursor.description, row))
            return row

    def __enter__(self):
        if not self._dbapi:
            self._close_on_exit = True
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._dbapi:
            return
        if exc_type:
            self.rollback()
        else:
            self.commit()
        if self._close_on_exit:
            self.close()


if __name__ == "__main__":
    dbi = MySQL_DBI_MySQLdb(connect=dict(host='localhost', user='test', password='test', database='test'))
    with dbi:
        with dbi.cursor('SELECT * FROM test') as cursor:
            for row in cursor:
                row = RowDict((d[0], v) for d, v in zip(cursor.description, row))
                print(row)

    with dbi:
        x = dbi.execute('INSERT INTO test () VALUES ()')
        print(x)

    with dbi:
        row = dbi.readone('SELECT * FROM test WHERE ID=%(ID)s', ID=1)
        print(row)
