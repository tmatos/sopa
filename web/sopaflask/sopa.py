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

@app.route('/addtarefa', methods=['GET', 'POST'])
def addtarefa():
    if request.method == 'POST':
        db = conexao()

        ida_origem = request.form['ida_origem']
        ida_destino = request.form['ida_destino']
        ida_data = request.form['ida_data']
        ida_adultos = int(request.form['ida_adultos'])
        ida_kids = int(request.form['ida_kids'])

        email = 'a@b'

        filtro_user = {'email': email}

        user = db.users.find_one(filtro_user)

        numero = user['seq_tarefa'] + 1

        db.users.update_one(
            filtro_user,
            {'$set': {'seq_tarefa': numero}}
        )

        objeto = {
            "email" : email,
            "numero" : numero,
            "periodo" : 24,
            "code" : {
                "request" : {
                    "slice" : [
                        {
                            "origin" : ida_origem,
                            "date" : ida_data,
                            "destination" : ida_destino
                        }#,
                        #{
                        #    "origin" : volta_origem,
                        #    "date" : volta_data,
                        #    "destination" : volta_destino
                        #}
                    ],
                    "passengers" : {
                        "adultCount" : ida_adultos,
                        "childCount" : ida_kids
                    },
                    "solutions" : 1
                }
            }
        }

        db.tarefas.insert_one(objeto)

        return redirect(url_for('tarefas'))
    else:
        return render_template('addtarefa.html')
    
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

    filtro = {'tarefa': int(tarefa)}
    cur = db.pontos.find(filtro).sort('_id', 1)
    
    lista = []

    for it in cur:
        if 'tripOption' in it['response']['trips']:
            str_valor = it['response']['trips']['tripOption'][0]['saleTotal']
            valor = float(str_valor[3:])
            ponto = { 'x': str(it['time']), 'y': valor }
            lista.append(ponto)
    
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