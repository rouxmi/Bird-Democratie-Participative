import sqlite3
from sqlite3.dbapi2 import Cursor
import os 
from flask import Flask, render_template, request, url_for,redirect,flash,session
import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="file_system"
app.config["IMAGE_UPLOADS"] = "static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

app.secret_key=os.urandom(12)

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def test_id_sub(id):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute(""" SELECT description FROM subs WHERE numéro_projet=?;""",(id,))
     test=cursor.fetchall()
     if test!=[]:
          return True
     else: 
          return False


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
     if test_id_sub(id):
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
     if test_id_sub(id):
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
     if test_id_sub(id):
          query = '''SELECT id_post,titre,description,id_sub,date_creation FROM posts WHERE id_sub=? ORDER BY date_creation;'''
          cursor.execute(query,(id,))
          L =(cursor.fetchall(),id)
          comments={}
          for row in L[0]:
               idpost=row[0]
               cursor.execute('SELECT contenu,posté_par FROM commentaires WHERE id_post=?',(idpost,))
               comments[idpost]=cursor.fetchall()
          return render_template('viewpost.html', data=L,comments=comments)
     else:
          db.close()
          return redirect('/')


@app.route('/sub/<id>/creationpost')
def newpost(id):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     if test_id_sub(id):
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
     if test_id_sub(id):
          if request.method=='POST':
               cursor.execute("INSERT INTO posts(id_sub,titre,description,date_creation,ratio) values(?,?,?,?,?)",(id,titre,description,datetime.date.today(),0))
               cursor.execute("SELECT max(id_post) FROM posts")
               idpost=cursor.fetchall()
               db.commit()
               db.close()
               if "image" in request.files:
                    image = request.files["image"]
                    split_tup = os.path.splitext(image.filename)
                    file_extension = split_tup[1]
                    if image.filename == "":
                         print("pas de nom")
                         return redirect('/sub/'+str(id)+'/creationpost')

                    if allowed_image(image.filename):
                         image.save(os.path.join(app.config["IMAGE_UPLOADS"], str(idpost[0][0])+str(file_extension)))
                         print("image sauvegardé")
                         return redirect('/sub/'+str(id)+'/creationpost')
                    
                    else:
                         print("type de fichier non supporté")
                         return redirect('/sub/'+str(id)+'/creationpost')
               return redirect('/sub/'+str(id)+'/creationpost')
          return render_template('newpost.html')
     else:
          db.close()
          return redirect('/')
     


@app.route('/<id>/ajoutcompteur')
def updatecompteurpostpositif(id):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     if test_id_sub(id):
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
     if test_id_sub(id):
          cursor.execute("UPDATE posts SET ratio= ratio -1 WHERE id_post=?",(id,))
          db.commit()
          db.close()
          return redirect('/')
     else:
          db.close()
          return redirect('/')

@app.route('/profil')
def voirleprofil():
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute("SELECT niveau FROM utilisateurs WHERE id_user=?",(str(session.get("id"))))
     niveau=cursor.fetchall()
     if niveau[0][0]=='A':
          return render_template('profil.html',data='e')
     else:
          return render_template('profil.html',data=1)

@app.route('/validation')
def validation_utilisateur():
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute("SELECT niveau FROM utilisateurs WHERE id_user=?",(str(session.get("id"))))
     niveau=cursor.fetchall()
     if niveau[0][0]=='A':
          cursor.execute('SELECT niveau,id_user,nom,prénom FROM utilisateurs')
          data=cursor.fetchall()
          return render_template('validation.html',data=data,admin=str(session.get("id")))
     else:
          return redirect('/')

@app.route('/<id>/<admin>/<niveau>')
def update_niveau(id,admin,niveau):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute("SELECT niveau FROM utilisateurs WHERE id_user=?",(str(id)))
     niv=cursor.fetchall()
     cursor.execute("SELECT niveau FROM utilisateurs WHERE id_user=?",(str(admin)))
     user=cursor.fetchall()
     if user[0][0]=='A' and niv!=[]:
          if niveau=='Admin':
               cursor.execute("UPDATE utilisateurs SET niveau='A' WHERE id_user=?",(str(id),))
               db.commit()
               db.close()
               return redirect('/validation')
          elif niveau=='Validé':
               cursor.execute("UPDATE utilisateurs SET niveau='V' WHERE id_user=?",(str(id),))
               db.commit()
               db.close()
               return redirect('/validation')
          else:
               return redirect('/')
     else:
          db.close()
          return redirect('/')

     
@app.route('/comment/<id>',methods=['post'])
def post_commentaire(id):
     content=request.form.to_dict()
     print(content)
     if request.method=='POST':
          db = sqlite3.connect('database.db')
          cursor = db.cursor()
          cursor.execute('INSERT INTO commentaires(contenu,posté_par,id_post) VALUES (?,?,?)',(content['commentaire'],str(session.get('id')),id))
          db.commit()
          db.close()
     return redirect('/sub/'+str(id)+'/post')

if __name__=='__main__':
     app.run(debug=1)
