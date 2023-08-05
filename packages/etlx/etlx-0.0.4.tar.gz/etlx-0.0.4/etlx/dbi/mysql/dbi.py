import MySQLdb

class MySQL_DBI:

    def __init__(self, connect):
        self._connect_kwargs = dict()
        self._connect_kwargs.update(connect)
        self._dbapi = None
        self._close_on_exit = False

    @property
    def database(self):
        return self._connect_kwargs.get('database')

    def _kwargs(self, config, kwargs):
        result = dict()
        result.update(config)
        result.update(kwargs)
        result = filter(lambda x: bool(x[1]), result.items())
        result = dict(result)
        return result

    def connect(self, **kwargs):
        kwargs = self._kwargs(self._connect_kwargs,kwargs)
        self._dbapi = MySQLdb.connect(**kwargs)
    
    def close(self):
        if self._dbapi:
            self._dbapi.close()
            self._dbapi = None

    def cursor(self):
        return self._dbapi.cursor(cursorclass=MySQLdb.cursors.SSCursor)
    
    def commit(self):
        self._dbapi.commit()

    def rollback(self):
        if self._dbapi:
            self._dbapi.rollback()

    def execute(self, sql):
        if not isinstance(sql,str):
            sql = str(sql)
        with self.cursor() as cursor:
            cursor.execute(sql)

    def query(self, sql):
        if not isinstance(sql,str):
            sql = str(sql)
        cursor = self.cursor()
        try:
            cursor.execute(sql)
            return iter(cursor)
        except:
            cursor.close()
            raise

    def queryOne(self, sql):
        if not isinstance(sql,str):
            sql = str(sql)
        with self.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()

    def queryList(self, sql):
        if not isinstance(sql,str):
            sql = str(sql)
        with self.cursor() as cursor:
            cursor.execute(sql)
            return list(iter(cursor))

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
