"""
A module which:
1. to connect and disconnect to Users Database.
2. Return cursor and conn to user.
"""
import pymysql
from pypika import Table, Query
from kubernetes import client, config
import base64


def connect():
    # get secret from kubernetes cluster
    config.load_kube_config()
    v1 = client.CoreV1Api()
    secret = str(v1.read_namespaced_secret("db-pass", "default").data)
    username = str(base64.b64decode(secret.strip().split()[3].translate('}\''))).strip("b")
    password = str(base64.b64decode(secret.strip().split()[1].translate('}\''))).strip("b")

    conn = pymysql.connect(host='remotemysql.com', port=3306, user=username, passwd=password, db='BSqnOU0gA6')
    conn.autocommit(True)
    cursor = conn.cursor()

    return conn, cursor


def disconnect(conn, cursor):
    cursor.close()
    conn.close()


def select(table, select_value="*", where=None, conn=None, cursor=None):
    if where is None:
        where = []

    if conn is not None:  # if user wants to specify connection himself
        table_data = Table(table)
        if len(where) > 0:
            q = Query.from_(table_data).select(select_value).where(
                table_data.field(where[0]) == where[1]).get_sql().replace('"', "")
        else:
            q = Query.from_(table_data).select(select_value).get_sql().replace('"', "")

        value = cursor.execute(q)

        return value

    else:  # if he doesn't
        conn, cursor = connect()
        table_data = Table(table)
        if len(where) > 0:
            q = Query.from_(table_data).select(select_value).where(
                table_data.field(where[0]) == where[1]).get_sql().replace('"', "")
        else:
            q = Query.from_(table_data).select(select_value)

        value = cursor.execute(q)

        disconnect(conn, cursor)

        return value


def post(table, insert_values=None, conn=None, cursor=None):
    if insert_values is None:
        insert_values = []

    if conn is not None:  # if user wants to specify connection himself
        table_data = Table(table)
        q = Query.into(table_data).insert(insert_values).get_sql().replace('"', "")

        cursor.execute(q)

    else:  # if not
        connect()
        table_data = Table(table)
        q = Query.into(table_data).insert(insert_values).get_sql().replace('"', "")

        cursor.execute(q)

        disconnect(conn, cursor)


def put(table, field_value=None, where=None, conn=None, cursor=None):
    if where is None:
        where = []
    if field_value is None:
        field_value = {}

    try:
        if conn is not None:
            table_data = Table(table)

            q = Query.update(table_data).set(field_value[0], field_value[1]).where(
                table_data.field(where[0]) == where[1]).get_sql().replace('"', "")

            select(table, conn=conn, cursor=cursor)  # fetch cursor size
            before_put_rowcount = cursor.rowcount
            cursor.execute(q)

            select(table, conn=conn, cursor=cursor)  # fetch cursor size after insert
            if before_put_rowcount + 1 == cursor.rowcount:
                return "Success"
            else:
                return "Failed"

        else:
            conn, cursor = connect()
            table_data = Table(table)

            q = Query.update(table_data).set(field_value[0], field_value[1]).where(
                table_data.field(where[0]) == where[1]).get_sql().replace('"', "")

            select(table, conn=conn, cursor=cursor)  # fetch cursor size
            before_put_rowcount = cursor.rowcount
            cursor.execute(q)

            select(table, conn=conn, cursor=cursor)  # fetch cursor size after insert
            if before_put_rowcount + 1 == cursor.rowcount:
                disconnect(conn, cursor)
                return "Success"
            else:
                disconnect(conn, cursor)
                return "Failed"

    except pymysql.IntegrityError as err:
        return "Failed"


def delete(table, where, conn=None, cursor=None):
    if where is None:
        where = []

    if conn is not None:
        table_data = Table(table)
        q = Query.from_(table_data).delete().where(table_data.field(where[0]) == where[1]).get_sql().replace('"', "")

        select(table, conn=conn, cursor=cursor)  # fetch cursor size
        before_put_rowcount = cursor.rowcount
        cursor.execute(q)

        select(table, conn=conn, cursor=cursor)  # fetch cursor size after insert
        print(before_put_rowcount, cursor.rowcount)
        if before_put_rowcount - 1 == cursor.rowcount:
            return "Success"
        else:
            return "Failed"
    else:
        conn, cursor = connect()
        table_data = Table(table)
        q = Query.from_(table_data).delete().where(table_data.field(where[0]) == where[1]).get_sql().replace('"', "")

        select(table, conn=conn, cursor=cursor)  # fetch cursor size
        before_put_rowcount = cursor.rowcount
        cursor.execute(q)

        select(table, conn=conn, cursor=cursor)  # fetch cursor size after insert
        if before_put_rowcount - 1 == cursor.rowcount:
            disconnect(conn, cursor)
            return "Success"
        else:
            disconnect(conn, cursor)
            return "Failed"
