"""
This testing platform will test the backend API functionality to a given input from user.
The user inserts an ID and Username he wish to create and the testing will try to perform the POST and GET actions.
"""
import requests

from Project.Module.db_connector import connect
from Project.Module.db_connector import disconnect

from pypika import Table, Query

try:
    # Get inputs from user
    user_id = input("Insert requested id for entry creation: ")
    user_name = input("Enter a user name for database entry creation: ")

    # request a post action to store data inside the database
    requests.post("http://127.0.0.1:5000/users/{}".format(user_id), json={"user_name": user_name})

    # Check if user created successfully
    data = requests.get("http://127.0.0.1:5000/users/{}".format(user_id))
    print(data.status_code, data.json()["user_name"], user_name)
    if data.status_code == 200 and data.json()["user_name"] in user_name:
        print("\nStatus code is \'%i\' and user name is \'%s\' as requested by user.\n" % (data.status_code, user_name))

        # Connect to database and get cursor
        conn, cursor = connect()

        # Create table and select query
        users_dateTime = Table('BSqnOU0gA6.users_dateTime')
        q = Query.from_(users_dateTime).select("*").where(users_dateTime.field("user_id") == user_id).get_sql().replace('"', "")
        cursor.execute(q) # "SELECT * from BSqnOU0gA6.users_dateTime WHERE user_id = %s", args=user_id
        for row in cursor:
            print("User\'s ID and Name are \'%s\' and \'%s\' and the values the user asked for are ID \'%s\' and Name "
                  "\'%s\'." % (row[0], row[1], user_id, user_name))

        disconnect(conn, cursor)

    else:
        if data.status_code != 200:
            print("Status code is \'%i\', the user was not created as requested." % data.status_code)
            raise Exception("Test Failed")

        else:
            print("Status code is \'%i\', The user was created as requested at another ID because the ID requested "
                  "was already equipped" % data.status_code)

            # Connect to database and get cursor
            conn, cursor = connect()

            # Create table and select query
            users_dateTime = Table('BSqnOU0gA6.users_dateTime')
            q = Query.from_(users_dateTime).select("*").where(users_dateTime.field("user_id") == user_id).get_sql().replace('"', "")
            cursor.execute(q)  # "SELECT * from BSqnOU0gA6.users_dateTime WHERE user_id = %s", args=user_id
            for row in cursor:
                print(
                    "User\'s ID and Name are \'%s\' and \'%s\' and the values the user asked for are ID \'%s\' and "
                    "Name "
                    "\'%s\'." % (row[0], row[1], user_id, user_name))

            disconnect(conn, cursor)



except Exception as err:
    print("Test Failed")
