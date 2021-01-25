"""
This testing platform will test the Frontend API functionality to a given user ID.
Just run and enjoy :)
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Project.Module.db_connector import connect
from Project.Module.db_connector import disconnect

try:
    chrome = webdriver.Chrome(".\\chromedriver.exe")
    chrome.get("http://127.0.0.1:5001/get_user_name/1")
    WebDriverWait(chrome, 15).until(EC.presence_of_element_located((By.ID, "user")))
    print("User name fetched from server: ", chrome.find_element_by_id("user").text)

    chrome.close()

except Exception as err:
    print("Test Failed")
