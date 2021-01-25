"""
A module which:
1. to connect and disconnect to Users Database.
2. Return cursor and conn to user.
"""
import pymysql


def connect():
    conn = pymysql.connect(host='remotemysql.com', port=3306, user='BSqnOU0gA6', passwd='afk3ad3PXB', db='BSqnOU0gA6')
    conn.autocommit(True)
    cursor = conn.cursor()

    return conn, cursor


def disconnect(conn, cursor):
    cursor.close()
    conn.close()
