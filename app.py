import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/form')
def form():
     return render_template('sub.html')

@app.route('/post',methods=['post'])
def post():
     form_data=request.form.to_dict()
     print(form_data)
     subs = sqlite3.connect('sub.db')
     cursor = subs.cursor()
     cursor.execute("""
     INSERT INTO table1(Nom,Mots_clés) values(?,?)""",(str(form_data['name']),str(form_data['domaine'])))
     subs.commit()
     return render_template('sub.html')
    