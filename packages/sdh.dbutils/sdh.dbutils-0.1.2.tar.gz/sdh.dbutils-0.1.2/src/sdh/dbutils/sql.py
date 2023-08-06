from django.db.transaction import get_connection
from psycopg2.extras import DictCursor


def exec_sql(sql, vars=None, using=None):
    with get_connection(using).cursor() as cursor:
        cursor.execute(sql, vars)

        if cursor.rowcount > 0:
            return cursor.fetchone()


def exec_sql_modify(sql, vars=None, using=None):
    with get_connection(using).cursor() as cursor:
        cursor.execute(sql, vars)
        return cursor.rowcount


def iter_sql(sql, vars=None, using=None):
    with get_connection(using).cursor() as cursor:
        cursor.execute(sql, vars)
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row


def exec_sql_dict(sql, vars=None, using=None):
    with get_connection(using).cursor() as cursor:
        dict_cursor = cursor.cursor.connection.cursor(cursor_factory=DictCursor)
        dict_cursor.execute(sql, vars)
        if dict_cursor.rowcount > 0:
            return dict_cursor.fetchone()


def iter_sql_dict(sql, vars=None, using=None):
    with get_connection(using).cursor() as cursor:
        dict_cursor = cursor.cursor.connection.cursor(cursor_factory=DictCursor)
        dict_cursor.execute(sql, vars)
        while True:
            row = dict_cursor.fetchone()
            if row is None:
                break
            yield row


