#Time
from time import sleep
#Datetime
from datetime import datetime

# MongoDB connection
from pymongo import MongoClient
client = MongoClient('mongodb://root:example@localhost:27018')
db = client['pctf']
payloads = db.payloads
print("Connected to mongodb://localhost:27017")

# import webdriver 
from selenium import webdriver 
from selenium.webdriver.firefox.options import Options  
opts = Options()
opts.headless = True
print("Importing Webdriver successful")

while True:
    #Grab Unvisited Payloads
    print(f"Grabbing Payloads {datetime.now()}")
    unvisitedpayloads = payloads.find({"visited":False})

    for payload in unvisitedpayloads:
        # create webdriver object 
        driver = webdriver.Firefox(options=opts)
        #Set timeout
        driver.set_page_load_timeout(120)
        driver.get('http://localhost:8000')  
        driver.add_cookie({"name":"jwt", "value":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluMTMzN2JzQGJlYXV0aWZ1bHNpdGVzLmNvbSIsImlhdCI6MTYxMDQwMTE4OH0.QG_ahc3h6KlirfU4Uf6WgaPBJ0bMGVaWANHcrw46EZo"})
        driver.add_cookie({"name":"pragyan", "value": "2021"})

        id = payload['_id']
        name = payload["name"]
        dob = payload["dob"]
        education = payload["education"]
        job = payload["job"]
        email = payload["email"]
        url = f"http://localhost:8000/finalpreview?name={name}&dob={dob}&education={education}&job={job}&submit=Submit"
        print(f"Visiting payload by {email} ID:{id}")
        driver.get(url)
        payloads.update_one({ "_id" : id}, { "$set" :{"visited": True}})
        driver.quit()

    print("All Payloads Done. Waiting for 5 seconds before fetching")
    sleep(5)

    
