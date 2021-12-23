import sqlite3
from sqlite3.dbapi2 import Cursor
import os 
from flask import Flask, render_template, request, url_for,redirect,flash,session
import datetime


app = Flask(__name__)
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="file_system"
app.secret_key=os.urandom(12)


@app.route('/')
def login():
     if not session.get("id"):
          return render_template('login.html', message=1)
     else:
          return redirect('/accueil')

@app.route('/connect',methods=['post'])
def connect():
     form_data=request.form.to_dict()
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute(""" SELECT mdp FROM utilisateurs WHERE mail=?""",(str(form_data['username']),))
     verif=cursor.fetchall()
     if verif[0][0]==str(form_data['password']):
          cursor.execute(""" SELECT id_user,nom,prénom,mail FROM utilisateurs WHERE mail=?""",(str(form_data['username']),))
          id=cursor.fetchall()
          db.close()
          session['id']=id[0][0]
          session['nom']=id[0][1]
          session['prénom']=id[0][2]
          session['username']=id[0][3]
          session['password']=verif
          return redirect('/accueil')
     else:
          db.close()
          return render_template('login.html',message=str('Votre mail et/ou votre mot de passe sont erronés, veuillez réessayer'))

     

@app.route('/register')
def register():
     return render_template('register.html',message=1)


@app.route('/enregistrement',methods=['get','post'])
def enregistre():
     if request.method == 'POST':
          form=request.form.to_dict()
          db = sqlite3.connect('database.db')
          cursor = db.cursor()
          cursor.execute(""" SELECT nom FROM utilisateurs WHERE mail=?""",(str(form['mail']),))
          verif=cursor.fetchall()
          if verif!=[]:
               db.close()
               return render_template('register.html',message='mail déjà utilisé')
          else:
               cursor.execute(""" INSERT INTO utilisateurs(nom,prénom,mail,mdp,Niveau) values(?,?,?,?,?)""",(str(form['nom']),str(form['prénom']),str(form['mail']),str(form['mdp']),'A'))
               db.commit()
               db.close()
               return redirect('/')
     else:
          return redirect('/')

@app.route('/accueil')
def accueil():
     query = "SELECT nom,titre,posts.description,id_sub,posts.date_creation,id_post FROM subs JOIN posts WHERE Numéro_projet = id_sub ORDER BY date_creation DESC;"
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute(query)
     L = cursor.fetchall()
     db.close()
     return render_template('accueil.html',data = L)

@app.route('/form')
def form():
     return render_template('sub.html')

@app.route('/parcourir')
def parcourir():
     db='database.db'
     con=sqlite3.connect(db)
     cur=con.cursor()
     cur.execute("SELECT * FROM subs ORDER BY création DESC;")
     L=cur.fetchall()
     con.close()
     return render_template('parcourir.html',data=L)

@app.route('/post',methods=['post'])
def post():
     form_data=request.form.to_dict()
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     id=session.get('id')
     cursor.execute("""
     INSERT INTO subs(nom,posté_par,mots_clés,description,création) values(?,?,?,?,?)""",(str(form_data['name']),id,str(form_data['domaine']),str(form_data['description']),datetime.date.today()))
     db.commit()
     db.close()
     return redirect('/')


@app.route('/search', methods=['GET', 'POST'])
def recherche():
    search = request.form.to_dict()
    if request.method == 'POST':
        return search_results(search)
    return render_template('resultat.html', form=search)


@app.route('/results')
def search_results(search):
     resultat = []
     search_str = search['Search']
     subs = sqlite3.connect('database.db')
     cursor = subs.cursor()
     cursor.execute("""SELECT * FROM subs""")
     contenu=cursor.fetchall()
     resultat=[]
     for row in contenu:
          if search_str in row[0] or search_str in row[3]:
               date=row[5].split('-')
               Y=int(date[0])
               M=int(date[1])
               D=int(date[2])
               resultat.append(row[:-1]+(str((datetime.date.today()-datetime.date(Y,M,D)).days)+' days ago',))
               
     subs.close()
     if not resultat:
         return render_template('resultat.html',resultat='')
     else:
         return render_template('resultat.html', resultat=resultat)

@app.route('/sub/<id>')
def viewsub(id):
     subs = sqlite3.connect('database.db')
     cursor = subs.cursor()
     cursor.execute(""" SELECT description FROM subs WHERE numéro_projet=?""",(id,))
     test=cursor.fetchall()
     if test!=[]:
          cursor.execute("SELECT nom,description FROM subs WHERE numéro_projet=%s;" % id)
          L=(cursor.fetchall(),id)
          subs.close()
          return render_template('viewsub.html',data=L)
     else:
          subs.close()
          return redirect('/')

@app.route("/<id>/abonnement")
def abonnement(id):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute(""" SELECT description FROM subs WHERE numéro_projet=?;""",(id,))
     test=cursor.fetchall()
     if test!=[]:
          cursor.execute("INSERT INTO abonnements(sub,utilisateur) VALUES (?,?);",(id,session.get('id')))
          db.commit()
          db.close()
          return redirect(url_for('viewsub',id=id))
     else :
          db.close()
          return redirect('/')


     

@app.route('/sub/<id>/post')
def viewpost(id):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute(""" SELECT description FROM subs WHERE numéro_projet=?""",(id,))
     test=cursor.fetchall()
     if test!=[]:
          query = '''SELECT titre,description,id_sub,date_creation FROM posts WHERE id_sub=? ORDER BY date_creation;'''
          cursor.execute(query,id)
          L =(cursor.fetchall(),id)
          return render_template('viewpost.html', data=L)
     else:
          db.close()
          return redirect('/')


@app.route('/sub/<id>/creationpost')
def newpost(id):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute(""" SELECT description FROM subs WHERE numéro_projet=?""",(id,))
     test=cursor.fetchall()
     db.close()
     if test!=[]:
          return render_template('newpost.html',data=id)
     else:
          db.close()
          return redirect('/')

@app.route('/postsub/<id>',methods = ['GET','POST'])
def postsub(id):
     titre = request.form['titre']
     description = request.form['description']
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute(""" SELECT description FROM subs WHERE numéro_projet=?""",(id,))
     test=cursor.fetchall()
     if test!=[]:
          cursor.execute("INSERT INTO posts(id_sub,titre,description,date_creation,ratio) values(?,?,?,?,?)",(id,titre,description,datetime.date.today(),0))
          db.commit()
          db.close()
          return redirect('/')
     else:
          db.close()
          return redirect('/')
     


@app.route('/<id>/ajoutcompteur')
def updatecompteurpostpositif(id):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute(""" SELECT description FROM subs WHERE numéro_projet=?""",(id,))
     test=cursor.fetchall()
     if test!=[]:
          cursor.execute("UPDATE posts SET ratio= ratio +1 WHERE id_post=?",(id,))
          db.commit()
          db.close()
          return redirect('/')
     else:
          db.close()
          return redirect('/')

@app.route('/<id>/retraitcompteur')
def updatecompteurpostnegatif(id):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute(""" SELECT description FROM subs WHERE numéro_projet=?""",(id,))
     test=cursor.fetchall()
     if test!=[]:
          cursor.execute("UPDATE posts SET ratio= ratio -1 WHERE id_post=?",(id,))
          db.commit()
          db.close()
          return redirect('/')
     else:
          db.close()
          return redirect('/')

@app.route('/profil')
def voirleprofil():
     return render_template('profil.html')


if __name__=='__main__':
     app.run(debug=1)
