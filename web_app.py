"""
This is the frontend API.
The frontend API functionality is to return a Username which corresponds to a given user ID inserted to url by user.
If the user name is found in the users table, the API will return it.
Otherwise, it will return an error.
"""
from flask import Flask

from Project.Module.db_connector import connect
from Project.Module.db_connector import disconnect

from pypika import Table, Query

app = Flask(__name__)


@app.route("/get_user_name/<user_id>")
def get_user_name(user_id):
    # connect to database and get cursor
    conn, cursor = connect()

    # Create table and query using pypika
    users_dateTime = Table('BSqnOU0gA6.users_dateTime')
    q = Query.from_(users_dateTime).select("user_name").where(users_dateTime.field("user_id") == user_id).get_sql().replace('"', "")
    user_name = cursor.execute(q)  # SELECT user_name FROM BSqnOU0gA6.users_dateTime WHERE user_id = %s
    if user_name != 0:
        for row in cursor:
            disconnect(conn, cursor)
            return "<h1 id='user'>" + row[0] + "</h1>"
    else:
        return "<h1 id='error'>" + 'no such user: ' + user_id + "</h1>"


app.run(host='127.0.0.1', debug=True, port=5001)
