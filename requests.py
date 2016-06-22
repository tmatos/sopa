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

url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=' + config.key

while 1:
    cursor = db.tarefas.find()
    
    for it in cursor:
        code = it['code']
    
        jsonreq = json.dumps(code, encoding = 'utf-8')
        
        headers = {'Content-Type': 'application/json'}
        req = urllib2.Request(url, jsonreq, headers)
        
        flight = urllib2.urlopen(req)
        
        response = flight.read()
        flight.close()
        
        obj_resp = json.loads(response)
        obj_time = datetime.datetime.now()
        obj_ponto = { 'tarefa' : it['numero'], 'time' : obj_time, 'response' : obj_resp }
        texto = json.dumps(obj_ponto, default=json_util.default)
        
        # para debug
        #v_file = open('ssaGRU1.json', 'a')
        #v_file.write(texto)
        #v_file.close()
        
        
        # salva no banco
        db.pontos.insert_one(obj_ponto)
        
        print 'INFO: Obteve ponto da tarefa ', obj_ponto['tarefa']
    
    time.sleep(20)
