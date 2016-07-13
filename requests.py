# -*- coding: utf-8 -*-

import sys
import signal
import json
import time
import datetime

import urllib.request
from bson import json_util
from pymongo import MongoClient

import ssl

# configuracoes do programa
import config

# handler para control-c
def signal_handler(signal, frame):
    print('\nFinalizando')
    exit(0)
    
signal.signal(signal.SIGINT, signal_handler)

# mensagem
print('SOPA - Airfare optimization system')
print('Fares request service, 0.01 alpha')
print('')

# connect to database
try:
    connection = MongoClient(config.mongo_host, config.mongo_port)
    db = connection.SOPA1
    print('Usando o banco em: ' + config.mongo_host + '\n')
except:
    e = sys.exc_info()[0]
    print('ERRO ao conectar no banco de dados!')
    print(e)
    exit()

url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=' + config.key

while 1:
    cursor = db.tarefas.find()
    
    for it in cursor:
        if('last_query' in it):
            last_query = it['last_query']
        else:
            last_query = datetime.datetime.min

        if (last_query + datetime.timedelta(days=1)) < datetime.datetime.now():
            jsonreq = json.dumps(it['code']).encode('utf-8')
            headers = {'Content-Type': 'application/json'}
            req = urllib.request.Request(url, jsonreq, headers)

            ssl._create_default_https_context = ssl._create_unverified_context # por problema com certificados!!!!

            try:
                flight = urllib.request.urlopen(req) # , cafile='./certs/googleapis.pem') #FIXME
                response = flight.read().decode('utf-8')
                flight.close()
            except:
                print('ERRO: Nao obteve ponto da tarefa ', it['numero'])
                continue

            obj_resp = json.loads(response)
            obj_time = datetime.datetime.now() # mudar esta funcao quando for conveniente!!!!!!!!
            obj_ponto = { 'tarefa' : it['numero'], 'time' : obj_time, 'response' : obj_resp }

            # salva no banco
            db.pontos.insert_one(obj_ponto)

            # atualiza info na lista de tarefas
            db.tarefas.update_one(
                {'numero': it['numero']},
                {'$set': {'last_query': obj_time}}
            )

            print('INFO: Obteve ponto da tarefa ', it['numero'])
    
    time.sleep(20)
