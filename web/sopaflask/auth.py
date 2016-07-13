# -*- coding: utf-8 -*-

# funcoes para autenticacao do usuario

import uuid
import hashlib

def hash_password(password):
    salt = uuid.uuid4().hex # random number
    blob = salt.encode() + password.encode()
    return hashlib.sha512(blob).hexdigest() + ':' + salt
    
def valid_password(user_password, hashed_password):
    password, salt = hashed_password.split(':')
    blob = salt.encode() + user_password.encode()
    return password == hashlib.sha512(blob).hexdigest()
