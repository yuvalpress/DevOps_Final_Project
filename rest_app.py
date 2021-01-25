"""
This is the backend API.
The backend API functionality is to perform all basic method on the users table (GET, POST PUT and DELETE).
The user inserts a User ID to the url and the API responds to the request according to its method.
In case the method is:
GET - Returns the user name.
POST - Creates a user.
PUT - Updates a user which already exists in database.
DELETE - Deletes a user which already exists in database.
"""
from flask import Flask, request
from datetime import datetime

from Project.Module.db_connector import connect
from Project.Module.db_connector import disconnect

from pypika import Table, Query

app = Flask(__name__)


@app.route("/users/<user_id>", methods=['GET', 'POST', 'DELETE', 'PUT'])
def users_actions(user_id):
    if request.method == 'GET':
        try:
            # Connect to database and get cursor
            conn, cursor = connect()

            # Create table and query using pypika
            table = Table("BSqnOU0gA6.users_dateTime")
            q = Query.from_(table).select("*").where(table.field("user_id") == user_id).get_sql().replace('"', "")
            cursor.execute(q)  # "SELECT * FROM BSqnOU0gA6.users_dateTime WHERE user_id = %s", args=user_id
            for row in cursor:
                name = row[1]
                disconnect(conn, cursor) # Disconnect from Database

                return {"status": "ok", "user_name": name}, 200

        except Exception as err:
            return {"status": "error", "reason": "no such id"}, 500

    elif request.method == 'POST':  # Check if the method given os POST
        try:
            # Prepared Statement
            sql = "INSERT INTO BSqnOU0gA6.users_dateTime (user_id, user_name, creation_date) VALUES (%s, %s, %s)"

            # Connect to database and get cursor
            conn, cursor = connect()

            # Check if id exists and if it does it will get the next available id (1 above the last line in table)
            # Create table and query using pypika
            table = Table("BSqnOU0gA6.users_dateTime")
            q = Query.from_(table).select("*").where(table.field("user_id") == user_id).get_sql().replace('"', "")
            cursor.execute(q)  # "SELECT * FROM BSqnOU0gA6.users_dateTime WHERE user_id = %s" % user_id
            cursorLength = cursor.arraysize
            if cursorLength > 0:
                cursor.execute("SELECT * FROM BSqnOU0gA6.users_dateTime")
                last_id = (list(cursor)[-1])[0]
                user_id = last_id + 1

            data = request.json  # Get data from json payload
            date = datetime.now()  # Get current date and time for creation date field in users table

            # Create table and query using pypika
            table = Table("BSqnOU0gA6.users_dateTime")
            q = Query.into(table).insert(user_id, str(data.get("user_name")), date.strftime("%Y-%m-%d %H:%M:%S")).get_sql().replace('"', "")
            cursor.execute(q)  # sql, args=(user_id, str(data.get("user_name")), date.strftime("%Y-%m-%d %H:%M:%S"))

            # Disconnect from Database
            disconnect(conn, cursor)

            # If user generation succeeded
            return {"status": "ok", "user_added": data.get("user_name")}, 200

        except Exception as err:
            return {"status": "error", "reason": "id already exist"}, 500

    elif request.method == 'PUT':
        try:
            # Connect to database and get cursor
            conn, cursor = connect()

            data = request.json

            # Create table and query using pypika
            table = Table("BSqnOU0gA6.users_dateTime")
            q = Query.update(table).set(table.field("user_name"), data.get("user_name")).where(table.field("user_id") == user_id).get_sql().replace('"', "")
            cursor.execute(q)  # "UPDATE BSqnOU0gA6.users_dateTime SET user_name = %s WHERE user_id = %s",
            # args=(data.get("user_name"), user_id))

            # Disconnect from Database
            disconnect(conn, cursor)

            # Return json of success
            return {"status": "ok", "user_updated": data.get("user_name")}, 200

        except Exception as err:  # If error occurred
            return {"status": "error", "reason": "no such id"}, 500

    elif request.method == 'DELETE':
        try:
            # Connect to database and get cursor
            conn, cursor = connect()

            # Create table and query using pypika
            table = Table("BSqnOU0gA6.users_dateTime")
            q = Query.from_(table).delete().where(table.field("user_id") == user_id).get_sql().replace('"', "")
            cursor.execute(q) # "DELETE from BSqnOU0gA6.users_dateTime WHERE user_id = %s", args=user_id

            # Disconnect from Database
            disconnect(conn, cursor)

            # Return json of success
            return {"status": "ok", "user_deleted": user_id}, 200

        except Exception as err:  # If error occurred
            return {"status": "error", "reason": "no such id"}, 500


app.run(host='127.0.0.1', debug=True, port=5000)
