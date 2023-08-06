# file: ezmysql.py
# Author: eamonn
import pyodbc
import logging
from fuclib import MySql
import time


class SqlServerOdbc(object):

    def __init__(self, host, user, password, database, max_idle_time=5):
        self.host = host
        self.conn_info = 'DRIVER={SQL Server};DATABASE=%s;SERVER=%s;UID=%s;PWD=%s' % (database, host, user, password)
        self._db = None
        self._last_use_time = time.time()
        self.max_idle_time = float(max_idle_time)

        try:
            self.reconnect()
        except Exception:
            logging.error("Cannot connect to SqlServer on %s", self.host,
                          exc_info=True)

    def _ensure_connected(self):
        if (self._db is None or
                (time.time() - self._last_use_time > self.max_idle_time)):
            self.reconnect()
        self._last_use_time = time.time()

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()

    def reconnect(self):
        """Closes the existing database connection and re-opens it."""
        self.close()
        self._db = pyodbc.connect(self.conn_info, autocommit=True)

    def close(self):
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def __del__(self):
        self.close()

    def get(self, sqlStr, *args, close=True):
        """
        获取一条查询结果
        :param sqlStr:
        :return:
        """
        cursor = self._cursor()
        if "%s" in sqlStr:
            sqlStr = sqlStr.replace("%s", "?")
        cursor.execute(sqlStr, *args)
        data = cursor.fetchone()
        if close:
            cursor.close()
            return data

        return data, cursor

    def get_dict(self, sqlStr, *args):
        """
        导出一条查询结果，并转成字典类型
        :param sqlStr:
        :param args:
        :return:
        """
        if "%s" in sqlStr:
            sqlStr = sqlStr.replace("%s", "?")
        rows, cursor = self.get(sqlStr, *args, close=False)
        if rows:
            columns = [column[0] for column in cursor.description]
            cursor.close()
            return dict(zip(columns, rows))
        return dict()

    def query(self, sqlStr, *args, max_count=None, close=True):
        """
        获取全部查询结果
        :param sqlStr:
        :param max_count: 查询数据量
        :return:
        """
        cursor = self._cursor()
        if "%s" in sqlStr:
            sqlStr = sqlStr.replace("%s", "?")
        cursor.execute(sqlStr, *args)
        if max_count:
            data = cursor.fetchmany(max_count)
            if close:
                cursor.close()
                return data
            return data, cursor
        data = cursor.fetchall()
        if close:
            cursor.close()
            return data
        return data, cursor

    def query_dict(self, sqlStr, *args, max_count=None):
        """
        导出全部查询结果，并转成字典类型
        :param sqlStr:
        :param args:
        :param max_count:
        :return:
        """
        if "%s" in sqlStr:
            sqlStr = sqlStr.replace("%s", "?")
        results = list()
        rows, cursor = self.query(sqlStr, *args, max_count=max_count, close=False)
        columns = [column[0] for column in cursor.description]
        for row in rows:
            results.append(dict(zip(columns, row)))
        cursor.close()
        return results

    def query_page(self, sqlStr, *args, page_size=1000, page=1, close=True):
        """
        获取分页查询结果
        :param sqlStr:
        :param page: 页码
        :param page_size: 页码大小
        :return:
        """
        cursor = self._cursor()
        if "%s" in sqlStr:
            sqlStr = sqlStr.replace("%s", "?")
        cursor.execute(sqlStr, *args)
        cursor.skip((page - 1) * page_size)
        data = cursor.fetchmany(page_size)
        if close:
            cursor.close()
            return data
        return data, cursor

    def query_dict_page(self, sqlStr, *args, page_size=1000, page=1):
        """
        获取字典分页查询结果
        :param sqlStr:
        :param page: 页码
        :param page_size: 页码大小
        :return:
        """
        if "%s" in sqlStr:
            sqlStr = sqlStr.replace("%s", "?")
        results = list()
        rows, cursor = self.query_page(sqlStr, *args, page_size=page_size, page=page, close=False)
        columns = [column[0] for column in cursor.description]
        for row in rows:
            results.append(dict(zip(columns, row)))
        cursor.close()
        return results

    def count(self, sqlStr, *args):
        """
        获取查询条数
        :param sqlStr:
        :return:
        """
        cursor = self._cursor()
        import re
        pattern = re.compile("SELECT (.*?) FROM", re.IGNORECASE)
        result = re.findall(pattern, sqlStr)[0]
        sqlStr = sqlStr.replace(result, "count(0)", 1)
        if "%s" in sqlStr:
            sqlStr = sqlStr.replace("%s", "?")
        cursor.execute(sqlStr, *args)
        data = cursor.fetchone()[0]
        cursor.close()
        return data

    def execute(self, sqlStr, *args):
        """
        执行sql语句
        :param sqlStr:
        :param args:
        :return:
        """
        cursor = self._cursor()
        if "%s" in sqlStr:
            sqlStr = sqlStr.replace("%s", "?")
        cnt = cursor.execute(sqlStr, *args).rowcount
        cursor.close()
        return cnt

    def insert(self, table_name, item):
        """
        插入数据
        :param table_name:  数据表名
        :param item: 字典类型数据
        :return:
        """
        keys, values = zip(*item.items())
        sqlStr = None
        try:
            sqlStr = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, ",".join(keys), ",".join(["?"] * len(values)))
            self.execute(sqlStr, *values)
        except Exception as e:
            raise ValueError
            print(sqlStr)
            print(e)

    def insert_many(self, table_name, items):
        """
        插入多条数据
        :param table_name: 数据表名
        :param items: 列表类型数据
        :return:
        """
        if isinstance(items, list):
            for item in items:
                self.insert(table_name, item)

    def update(self, table_name, updates, search):
        """
        更新数据
        :param table_name: 表名
        :param updates:需要更新的字段
        :param search:查询条件
        :return:
        """
        upsets = []
        values = []
        for k, v in updates.items():
            s = '%s=?' % k
            upsets.append(s)
            values.append(v)
        upsets = ' , '.join(upsets)

        searchsets = []
        for k, v in dict(search).items():
            s = "%s='%s'" % (k, v)
            searchsets.append(s)
        searchsets = ' and '.join(searchsets)

        sqlStr = f'UPDATE %s SET %s WHERE {searchsets}' % (
            table_name,
            upsets
        )
        self.execute(sqlStr, *values)

