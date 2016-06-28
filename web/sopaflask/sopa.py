# -*- coding: utf-8 -*-

from auth import * # meu

import json
from flask import Flask, request, Response, redirect, render_template, url_for, flash
from pymongo import MongoClient

app = Flask("sopaflask")
app.secret_key = 'TrG&7gjrg98h@%$4g3#=#RG$W#9&q4658tn8q03-4ghq0*&tqj03m$W#9108dmb18t3%ID%e437'

def conexao():
    #connect to database
    con = MongoClient('localhost', 27017)
    db = con.SOPA1
    return db

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/help')
def help():
    return render_template('help.html')
    
@app.route('/tarefas')
def tarefas():
    db = conexao()
    
    cur = db.tarefas.find()
    dic = {}
    
    for it in cur:
        key = str(it['numero'])
        dic[key] = json.dumps(it['code'])
    
    return render_template('tarefas.html', result=dic)
    
@app.route('/historico')
def historico():
    db = conexao()
    
    cur = db.tarefas.find().sort('numero', 1)
    dic = {}
    
    for it in cur:
        key = str(it['numero'])
        dic[key] = "_id"
    
    return render_template('historico.html', lista=dic)

@app.route('/historico/<tarefa>')
def pontos(tarefa):
    db = conexao()
    
    cur = db.pontos.find( {'tarefa': int(tarefa)} ) 
    
    lista = []
    
    for it in cur:
        lista.append( str(it['time']) ) 
    
    return render_template('historico_detalhe.html', pontos=lista)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        db = conexao()
        user = db.users.find_one( {'email':email} )
        
        if user != None:
            if valid_password(senha, user['senha']):
                msg = 'Bem-vindo ' + user['nome'] + '!'
                flash(msg, 'info')
                return redirect(url_for('home'))
            else:
                erro = 'Credenciais inválidas.'
        else:
            erro = 'Usuário não cadastrado.'
    
    return render_template('login.html', erro=erro)
    
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.debug = True
    app.run()