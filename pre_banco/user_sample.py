
# criar a estrutura do banco

import uuid
import hashlib
import json
from bson import json_util
from pymongo import MongoClient


#connect to database
connection = MongoClient('localhost', 27017)
db = connection.SOPA1


# USUARIOS
nome = 'Tiago M'
email = 'a@b'
senha = '123'

def hash_password(password):
    salt = uuid.uuid4().hex # random number
    blob = salt.encode() + password.encode()
    return hashlib.sha512(blob).hexdigest() + ':' + salt
    
def valid_password(user_password, hashed_password):
    password, salt = hashed_password.split(':')
    blob = salt.encode() + user_password.encode()
    return password == hashlib.sha512(blob).hexdigest()
 
senha_hash = hash_password(senha)

usuario = {
            "nome" : nome,
            "email" : email,
            "senha" : senha_hash,
            "seq_tarefa" : 0       # sequencial pra guardar o indice maximo das tarefas desse usuario
        }

db.users.insert_one(usuario)
print('Inserido usuario: ' + nome)
