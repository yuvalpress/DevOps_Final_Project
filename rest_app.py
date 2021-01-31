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

from Module.db_connector import connect, disconnect, select, post, put, delete

import os
import signal

app = Flask(__name__)


def select_from_table(user_id):
    try:
        # Connect to database and get cursor
        conn, cursor = connect()

        select(table="BSqnOU0gA6.users_dateTime", where=["user_id", user_id], conn=conn,
               cursor=cursor)  # set the cursor

        name = None
        for row in cursor:
            name = row[1]
            disconnect(conn, cursor)  # Disconnect from Database

        if name is not None:
            return {"status": "ok", "user_name": name}, 200
        else:
            return {"status": "error", "reason": "no such id"}, 500

    except Exception as err:
        print(err)


def insert_into_table(user_id):
    try:
        # Prepared Statement
        sql = "INSERT INTO BSqnOU0gA6.users_dateTime (user_id, user_name, creation_date) VALUES (%s, %s, %s)"

        # Connect to database and get cursor
        conn, cursor = connect()

        # Check if id exists and if it does it will get the next available id (1 above the last line in table)
        select(table="BSqnOU0gA6.users_dateTime", where=["user_id", user_id], conn=conn, cursor=cursor)
        cursorLength = cursor.rowcount

        if cursorLength > 0:
            select(table="BSqnOU0gA6.users_dateTime", conn=conn, cursor=cursor)
            last_id = (list(cursor)[-1])[0]
            user_id = last_id + 1

        data = request.json  # Get data from json payload
        date = datetime.now()  # Get current date and time for creation date field in users table

        post("BSqnOU0gA6.users_dateTime", [user_id, str(data.get("user_name")), date.strftime("%Y-%m-%d %H:%M:%S")],
             conn=conn, cursor=cursor)

        # Disconnect from Database
        disconnect(conn, cursor)

        # If user generation succeeded
        return {"status": "ok", "user_added": data.get("user_name")}, 200

    except Exception as err:
        return {"status": "error", "reason": "id already exist"}, 500


def update_table(user_id):
    try:

        data = request.json
        answer = put("BSqnOU0gA6.users_dateTime", ["user_name", data.get("user_name")], ["user_id", user_id])

        # Return json of success of failure
        if answer == "Success":
            return {"status": "ok", "user_updated": data.get("user_name")}, 200
        else:
            return {"status": "error", "reason": "no such id"}, 500

    except Exception as err:  # If error occurred
        return {"status": "error", "reason": "no such id"}, 500


def delete_from_table(user_id):
    try:
        answer = delete("BSqnOU0gA6.users_dateTime", ["user_id", user_id])

        # Return json of success or failure
        if answer == "Success":
            return {"status": "ok", "user_deleted": user_id}, 200
        else:
            return {"status": "error", "reason": "no such id"}, 500

    except Exception as err:  # If error occurred
        return {"status": "error", "reason": "no such id"}, 500


@app.route("/users/<user_id>", methods=['GET', 'POST', 'DELETE', 'PUT'])
def users_actions(user_id):
    if request.method == 'GET':
        res = select_from_table(user_id)
        return res

    elif request.method == 'POST':  # Check if the method given os POST
        res = insert_into_table(user_id)
        return res

    elif request.method == 'PUT':
        res = update_table(user_id)
        return res

    elif request.method == 'DELETE':
        res = delete_from_table(user_id)
        return res

@app.route("/stop_server")
def stop_server():
    os.kill(os.getpid(), signal.CTRL_C_EVENT)

    return {"Result": "Server Stopped"}

app.run(host='127.0.0.1', debug=True, port=5000)
