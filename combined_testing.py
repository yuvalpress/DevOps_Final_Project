"""
This testing convention will try to operate both frontend and backend API's one after another.
Only if the Backend API behaves as expected then the Frontend API testing will be executed.
User to add data will be fetched from last line of config table.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
from pypika import Query, Table, Field

from Project.Module.db_connector import connect
from Project.Module.db_connector import disconnect

from pypika import Table, Query
# Backend check part
try:
    # Connect to database and get cursor
    conn, cursor = connect()

    # Get all data from config table
    q = Query.from_('BSqnOU0gA6.config').select("*").get_sql().replace('"', "")  # "SELECT * FROM BSqnOU0gA6.config"
    cursor.execute(q)
    last_line = list(cursor)[cursor.arraysize]

    user_id = input("Insert requested id for entry creation: ")
    http_link = str(last_line[1])
    browser = str(last_line[2])
    user_name = str(last_line[3])

    # request a post action to store data inside the database
    requests.post("%s/%s" % (http_link, user_id), json={"user_name": user_name})

    # Check if user created successfully
    data = requests.get("%s/%s" % (http_link, user_id))
    if data.status_code == 200 and data.json()["user_name"] == user_name:
        print("Status code is \'%i\', Data retrieved from REST API is the same as posted" % data.status_code)

        # Check if user requested to be created by user is stored under the requested id
        # Create table and query using pypika
        table = Table("BSqnOU0gA6.users_dateTime")
        q = Query.from_(table).select("*").where(table.field("user_id") == user_id)
        cursor.execute(q) # "SELECT * from BSqnOU0gA6.users_dateTime WHERE user_id = %s", args=user_id
        for row in cursor:
            print("User\'s ID and Name are \'%s\' and \'%s\' and the values the user asked for are ID \'%s\' and Name "
                  "\'%s\'." % (row[0], row[1], user_id, user_name))

        # Disconnect from database
        disconnect(conn, cursor)

        # Frontend check part
        if browser == "chrome" or browser == "Chrome":
            chrome = webdriver.Chrome(".\\chromedriver.exe")
            chrome.get("http://127.0.0.1:5001/get_user_name/%s" % user_id)
            WebDriverWait(chrome, 15).until(EC.presence_of_element_located((By.ID, "user")))
            print("User name fetched from server:", chrome.find_element_by_id("user").text + ",",
                  "Same as user requested at POST: %s" % user_name)

            chrome.close()

    else:
        if data.status_code != 200:
            print(
                "Status code is \'%i\', Data retrieved from REST API is not the same as the data posted." % data.status_code)
            raise Exception("Test Failed")

        else:
            print("Status code is \'%i\', User was created inside table but with another ID." % data.status_code)

            # Get the last user created (the last id as created in post method)
            # Create table and query using pypika
            table = Table("BSqnOU0gA6.users_dateTime")
            q = Query.from_(table).select("*").get_sql().replace('"', "")

            cursor.execute(q) # "SELECT * from BSqnOU0gA6.users_dateTime"
            data = list(cursor)[-1]
            print(
                "User\'s ID and Name are \'%s\' and \'%s\' and the values the user asked for are ID \'%s\' and Name "
                "\'%s\'." % (data[0], data[1], user_id, user_name))

            # Disconnect from database
            disconnect(conn, cursor)

            # Frontend check part
            if browser == "chrome" or browser == "Chrome":
                chrome = webdriver.Chrome(".\\chromedriver.exe")
                chrome.get("http://127.0.0.1:5001/get_user_name/%s" % data[0])
                WebDriverWait(chrome, 15).until(EC.presence_of_element_located((By.ID, "user")))
                print("User name fetched from server:", chrome.find_element_by_id("user").text + ",",
                      "Same as user requested at POST: %s" % user_name)

                chrome.close()


except Exception as err:
    print(err)
