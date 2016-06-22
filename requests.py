# -*- coding: utf-8 -*-

import urllib
import urllib2
import json
import time
import datetime

from bson import json_util
from pymongo import MongoClient

# configuracoes do programa
import config

#connect to database
connection = MongoClient('localhost', 27017)

db = connection.SOPA1

while 1:    
    url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + config.key
    
    code = {
        "request": {
            "passengers": {
                "adultCount": 1,
                "childCount": 0
            },
            "slice": [
                {
                    "origin": "SSA",
                    "destination": "GRU",
                    "date": "2016-07-19",
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
                    "date": "2016-12-25",
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
    
    headers = {'Content-Type': 'application/json'}
    req = urllib2.Request(url, jsonreq, headers)
    
    flight = urllib2.urlopen(req)
    
    response = flight.read()
    flight.close()
    
    obj_resp = json.loads(response)
    obj_time = datetime.datetime.now()
    obj_ponto = { "tarefa" : 1, "time" : obj_time, "response" : obj_resp }
    texto = json.dumps(obj_ponto, default=json_util.default)
    
    # para debug
    #v_file = open("ssaGRU1.json", "a")
    #v_file.write(texto)
    #v_file.close()
    
    
    # salva no banco
    db.pontos.insert_one(obj_ponto)
    
    print 'INFO: Obteve ponto da tarefa ', obj_ponto["tarefa"]
    
    time.sleep(20)
