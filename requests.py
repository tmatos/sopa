import urllib
import urllib2
import json
import time
import os
import pymongo

from pymongo import MongoClient

#connect to database
connection = MongoClient ('localhost', 27017)

db = connection.SOPA1

collection = db.SOPA1

while 1:    
    url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=AIzaSyA3758yM14aTX7aI9_v5AvKI2X1m56HszI" 
    
    code = {
        "request": {
            "passengers": {
                "adultCount": 1,
                "childCount": 1
            },
            "slice": [
                {
                    "origin": "SSA",
                    "destination": "GRU",
                    "date": "2015-12-19",
                    "permittedDepartureTime":
                    {
                        "kind": "qpxexpress#timeOfDayRange",
                        "earliestTime": "22:00",
                        "latestTime": "23:00"
                    }
                },
                {
                    "origin": "GRU",
                    "destination": "SSA",
                    "date": "2015-12-25",
                    "permittedDepartureTime":
                    {
                        "kind": "qpxexpress#timeOfDayRange",
                        "earliestTime": "05:00",
                        "latestTime": "12:00"
                    }
                }
            ],
            "solutions": 3
        }
    }
    
    
    jsonreq = json.dumps(code, encoding = 'utf-8')
    req = urllib2.Request(url, jsonreq, {'Content-Type': 'application/json'})
    flight = urllib2.urlopen(req)
    response = flight.read()
    flight.close()
    #print(response)
    print("----------------")
    
    
    texto=(response)
    v_file= open("ssaGRU1.json" ,"a")
    
    
    v_file.write(texto)
    v_file.close()
    
    time.sleep(0.7) 
    os.system("mongoimport --db SOPA1 --collection SOPA1 <ssaGRU1.json")
    
    
    time.sleep(15)
    

current_time = time.strftime("%H:%M", time.localtime())
v_file = open("ssaGRU.json", "a")
v_file.write(str(current_time) + ' : ')
v_file.write( '\n')
v_file.close()
