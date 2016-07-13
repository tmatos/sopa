
# criar a estrutura do banco

import json
from bson import json_util
from pymongo import MongoClient


#connect to database
connection = MongoClient('localhost', 27017)
db = connection.SOPA1

code = {
        'request': {
            'passengers': {
                'adultCount': 1,
                'childCount': 0
            },
            'slice': [
                {
                    'origin': 'SSA',
                    'destination': 'GRU',
                    'date': '2016-07-19',
                    'permittedDepartureTime':
                    {
                        'kind': 'qpxexpress#timeOfDayRange',
                        'earliestTime': '22:00',
                        'latestTime': '23:00'
                    }
                },
                {
                    'origin': 'GRU',
                    'destination': 'SSA',
                    'date': '2016-12-25',
                    'permittedDepartureTime':
                    {
                        'kind': 'qpxexpress#timeOfDayRange',
                        'earliestTime': '05:00',
                        'latestTime': '12:00'
                    }
                }
            ],
            'solutions': 3
        }
    }
    
code2 = {
        'request': {
            'passengers': {
                'adultCount': 1
            },
            'slice': [
                {
                    'origin': 'SSA',
                    'destination': 'GRU',
                    'date': '2016-07-19'
                },
                {
                    'origin': 'GRU',
                    'destination': 'SSA',
                    'date': '2016-12-25'
                }
            ],
            'solutions': 3
        }
    }

tarefa = {
            'numero' : 1,
            'email' : 'tiago_c@msn.com',
            'code' : code,
            'last_query' : None,
            'periodo' : 24
         }

db.tarefas.insert_one(tarefa)
print('Collection "tarefas" criado com um item de exemplo')

tarefa = {
            'numero' : 2,
            'email' : 'tiago_c@msn.com',
            'code' : code2,
            'last_query' : None,
            'periodo' : 24
        }

db.tarefas.insert_one(tarefa)
print('Add item 2 a collection "tarefas", outro exemplo mais simples ainda')
