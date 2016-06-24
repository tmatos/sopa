# -*- coding: utf-8 -*-

import json
from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/tarefas')
def tarefas():
    #connect to database
    con = MongoClient('localhost', 27017)
    db = con.SOPA1
    
    cur = db.tarefas.find()
    # out = ''
    dic = {}
    
    for it in cur:
        key = str(it['numero'])
        dic[key] = json.dumps(it['code'])
        
        # out += '<b>Tarefa:</b> ' + str(it['numero']) + '<br>'
        # out += '<b>Code: </b>' + json.dumps(it['code']) + '<br><br>'
    
    # return out
    
    return render_template('tarefas.html', result=dic)
    
@app.route('/pontos/<tarefa>')
def pontos(tarefa):
    #connect to database
    con = MongoClient('localhost', 27017)
    db = con.SOPA1
    
    cur = db.pontos.find( {'tarefa': int(tarefa)} )
    
    out = ''
    
    for it in cur:
        out += 'Em: ' + str(it['time']) + '<br>'
    
    return out

if __name__ == '__main__':
    app.debug = True
    app.run()