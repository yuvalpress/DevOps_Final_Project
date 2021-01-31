"""
This is the frontend API.
The frontend API functionality is to return a Username which corresponds to a given user ID inserted to url by user.
If the user name is found in the users table, the API will return it.
Otherwise, it will return an error.
"""
from flask import Flask

from Module.db_connector import connect
from Module.db_connector import disconnect
from Module.db_connector import select

from pypika import Table, Query

app = Flask(__name__)


@app.route("/get_user_name/<user_id>")
def get_user_name(user_id):

    # user db_connection library to select data from db
    conn, cursor = connect()
    user_name = select(table='BSqnOU0gA6.users_dateTime', select_value="*", where=["user_id", user_id], conn=conn, cursor=cursor)  # SELECT user_name FROM BSqnOU0gA6.users_dateTime WHERE user_id = %s
    if user_name != 0:
        for row in cursor:
            disconnect(conn, cursor)
            return "<h1 id='user'>" + row[1] + "</h1>"
    else:
        disconnect(conn, cursor)
        return "<h1 id='error'>" + 'no such user: ' + user_id + "</h1>"


app.run(host='127.0.0.1', debug=True, port=5001)
