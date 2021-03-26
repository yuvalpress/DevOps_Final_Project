"""
This testing platform will test the backend API functionality to a given input from user.
The user inserts an ID and Username he wish to create and the testing will try to perform the POST and GET actions.
"""
import requests

from Module.db_connector import connect, disconnect, select

try:
    # Get inputs from user
    user_id = 2
    user_name = "yuval press"

    # request a post action to store data inside the database
    url = ""
    with open("k8s_url.txt", "r") as file:
        for line in file:
            url = line

    requests.post("{}/users/{}".format(url, user_id), json={"user_name": user_name})

    # Check if user created successfully
    data = requests.get("{}/users/{}".format(url, user_id))
    if data.status_code == 200 and data.json()["user_name"] in user_name:
        print("\nStatus code is \'%i\' and user name is \'%s\' as requested by user.\n" % (data.status_code, user_name))

        # Connect to database and get cursor
        conn, cursor = connect()

        # Create table and select query
        select('BSqnOU0gA6.users_dateTime', where=["user_id", user_id], conn=conn, cursor=cursor)
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
                  "was already equipped \n" % data.status_code)

            # Connect to database and get cursor
            conn, cursor = connect()

            # Create table and select query
            select('BSqnOU0gA6.users_dateTime', conn=conn, cursor=cursor)
            line = list(cursor)[-1]
            print(
                "User\'s ID and Name are \'%s\' and \'%s\' and the values the user asked for are ID \'%s\' and "
                "Name "
                "\'%s\'." % (line[0], line[1], user_id, user_name))

            disconnect(conn, cursor)


except Exception as err:
    print("Test Failed")
