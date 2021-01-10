#Time
from time import sleep
#Datetime
from datetime import datetime

# MongoDB connection
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['pctf']
payloads = db.payloads
print("Connected to mongodb://localhost:27017")

# import webdriver 
from selenium import webdriver 
from selenium.webdriver.firefox.options import Options  
opts = Options()
opts.headless = False
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
        driver.add_cookie({"name":"jwt", "value":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImlhdCI6MTYxMDI4MTMyN30.zwt6ckzs0ND4yDw6nazHZU3o4i6nCO4frw5FTMMLcck"})
        driver.add_cookie({"name":"pragyan", "value": "2020"})

        id = payload['_id']
        name = payload["name"]
        dob = payload["dob"]
        education = payload["education"]
        job = payload["job"]
        url = f"http://localhost:8000/finalpreview?name={name}&dob={dob}&education={education}&job={job}&submit=Submit"
        
        driver.get(url)
        payloads.update_one({ "_id" : id}, { "$set" :{"visited": True}})
        driver.quit()

    print("All Payloads Done. Waiting for 5 seconds before fetching")
    sleep(5)

    
