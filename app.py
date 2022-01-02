import sqlite3
from sqlite3.dbapi2 import Cursor
import os 
from flask import Flask, render_template, request, url_for,redirect,flash,session
import datetime
from recommandation import recommandation
from werkzeug.utils import secure_filename
import time




app = Flask(__name__)

@app.context_processor
def handle_context():
    return dict(os=os)
    
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
     cursor.execute(""" SELECT description FROM subs WHERE numéro_projet=?""",(id,))
     test=cursor.fetchall()
     db.close()
     if test!=[]:
          return True
     else: 
          return False
     

def test_login():
     if session.get("id")!=None:
          return True
     else:
          return False
     
def test_verif():
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute(""" SELECT niveau FROM utilisateurs WHERE id_user=?""",(str(session.get('id')),))
     test=cursor.fetchall()[0][0]
     db.close()
     if test=='B':
          return False
     else:
          return True



def is_owner(id,user):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute(""" SELECT * FROM subs WHERE numéro_projet=? AND créé_par=?""",(id,user))
     test=cursor.fetchall()
     db.close()
     if test!=[]:
          return True
     else: 
          return False

def est_abonne(id,user):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute(""" SELECT * FROM abonnements WHERE sub=? AND utilisateur=?""",(id,user))
     test=cursor.fetchall()
     db.close()
     if test!=[]:
          return True
     else: 
          return False

def est_participant(id,user):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute(""" SELECT * FROM participants WHERE sub=? AND utilisateur=?""",(id,user))
     test=cursor.fetchall()
     db.close()
     if test!=[]:
          return True
     else: 
          return False

def a_demande(id,user):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute(""" SELECT * FROM demande_participation WHERE sub=? AND utilisateur=?""",(id,user))
     test=cursor.fetchall()
     db.close()
     if test!=[]:
          return True
     else: 
          return False

def commentaire(id_com,user):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute("SELECT likeur FROM commentaires WHERE id_commentaire=?",(id_com,))
     likeur=cursor.fetchall()
     db.close()
     if user not in likeur[0][0].split('/'):
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


# Route lié à la page d'accueil qui affiche le fil d'actualité
@app.route('/accueil')
def accueil():
     # Sélection des posts liés aux projets abonnés et créés par l'utilisateur, tri par ordre décroissant de date de création
     query = "SELECT DISTINCT nom,titre,posts.description,id_sub,posts.date_creation,id_post FROM subs JOIN posts JOIN abonnements WHERE Numéro_projet = id_sub AND (utilisateur=? AND sub=id_sub OR créé_par= ?) ORDER BY date_creation DESC"
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     id_user = session.get('id')
     cursor.execute(query,(id_user,id_user))
     L = cursor.fetchall()
     db.close()
     os.path.isfile("static/img/uploads/")
     return render_template('accueil.html',data = L)

@app.route('/form')
def form():
     if test_verif:
          return render_template('sub.html')
     else:
          return render_template('erreur.html',message="Accès refusé",description="vous n'avez pas les droits d'accès nécessaires")     

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
     if test_login():
          if test_verif():
               form_data=request.form.to_dict()
               db = sqlite3.connect('database.db')
               cursor = db.cursor()
               id=session.get('id')
               cursor.execute("""
               INSERT INTO subs(nom,créé_par,mots_clés,description,création) values(?,?,?,?,?)""",(str(form_data['name']),id,str(form_data['domaine']),str(form_data['description']),datetime.date.today()))
               db.commit()
               db.close()
               return redirect('/')
          else:
               return render_template('erreur.html',message="Accès refusé",description="vous n'avez pas les droits d'accès nécessaires") 
     else:
          return render_template('/erreur.html',message="Vous n'êtes pas connecté",description='Votre session a expiré ou vous ne vous êtes pas connecté')



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

@app.route('/recommandation')
def recom():
     if test_login():
          if test_verif():
               db = sqlite3.connect('database.db')
               cursor = db.cursor()
               cursor.execute("SELECT sub FROM abonnements INNER JOIN subs ON abonnements.sub=subs.numéro_projet WHERE utilisateur=?",(str(session.get("id"))))
               abonnement=cursor.fetchall()
               cursor.execute("SELECT numéro_projet FROM subs WHERE créé_par=?",(str(session.get("id"))))
               abonnement+=cursor.fetchall()
               total={}
               for i in range(len(abonnement)):
                    abonnement[i]=abonnement[i][0]
               for i in range(len(abonnement)):
                    temp=recommandation(abonnement[i])
                    for j in range(len(temp)):
                         if temp[j][0] not in abonnement:
                              if temp[j][0] in total:
                                   total[temp[j][0]]+=temp[j][1]
                              else:
                                   total[temp[j][0]]=temp[j][1]
               result=list(sorted(total.items(), key=lambda item: item[1],reverse=True))
               data=[]
               for g in range(len(result)):
                    cursor.execute("SELECT * FROM subs WHERE numéro_projet=?",(result[g][0],))
                    data.append(cursor.fetchall()[0]+(result[g][1],g+1))
               db.close()
               return render_template('recommandation.html',data=data)
          else:
               return render_template('erreur.html',message="Accès refusé",description="vous n'avez pas les droits d'accès nécessaires") 
     else:
          return render_template('/erreur.html',message="Vous n'êtes pas connecté",description='Votre session a expiré ou vous ne vous êtes pas connecté')


@app.route('/sub/<id>')
def viewsub(id):
     if test_login():
          db = sqlite3.connect('database.db')
          cursor = db.cursor()
          if test_id_sub(id):
               # Récupération des données liées au projet (nom,description, créateur, nombre d'abonnés, participants...)
               cursor.execute("SELECT subs.nom,description,créé_par,utilisateurs.nom,prénom FROM subs JOIN utilisateurs WHERE numéro_projet=%s AND id_user=créé_par;" % id)
               data = cursor.fetchall()
               cursor.execute("SELECT COUNT(*) FROM abonnements WHERE sub=?",(id,))
               nb_abonnes = cursor.fetchall()[0]
               cursor.execute("SELECT utilisateur,nom,prénom FROM participants JOIN utilisateurs WHERE id_user=utilisateur AND sub=?",(id,))
               liste_participants=cursor.fetchall()
               user_id = session.get('id')
               # Définition de l'état de l'utilisateur vis-à-vis du projet
               owner = is_owner(id,user_id)
               abonne = est_abonne(id,user_id)
               participant = est_participant(id,user_id)
               demande = a_demande(id,user_id)
               db.close()
               print(data)
               return render_template('viewsub.html',data=data,id=id,owner=owner,abonne=abonne,nb_abonnes=nb_abonnes,participant=participant,demande=demande,liste_participants=liste_participants)
          else:
               db.close()
               return redirect('/')
     else:
          return render_template('/erreur.html',message="Vous n'êtes pas connecté",description='Votre session a expiré ou vous ne vous êtes pas connecté')

#Route lié au bouton s'abonner du projet de numéro 'id'
@app.route("/<id>/abonnement")
def abonnement(id):
     if test_login() :
          if test_verif():
               if test_id_sub(id):
                    user = session.get('id')
                    if not is_owner(id,user) and not est_abonne(id,user):
                         db = sqlite3.connect('database.db')
                         cursor = db.cursor()
                         cursor.execute("INSERT INTO abonnements(sub,utilisateur) VALUES (?,?);",(id,session.get('id')))
                         db.commit()
                         db.close()
                         return redirect(url_for('viewsub',id=id))
                    else:
                         return render_template('erreur.html',message="Impossible de s'abonner",description="Vous êtes déjà abonné ou bien alors c'est votre projet")
               else :
                    return redirect('/')
          else:
               return render_template('erreur.html',message="Accès refusé",description="Vous n'avez pas les droits d'accès nécessaires") 
     else:
          return redirect('/')


# Route liée au bouton se désabonner du projet de numéro 'id'
@app.route('/<id>/desabonnement')
def desabonnement(id):
     if test_login():
          if test_verif():
               if test_id_sub(id):
                    user = session.get('id')
                    if est_abonne(id,user):
                         db = sqlite3.connect('database.db')
                         cursor = db.cursor()
                         cursor.execute("DELETE FROM abonnements WHERE sub=? AND utilisateur = ?;",(id,user))
                         if a_demande(id,user):
                              cursor.execute("DELETE FROM demande_participation WHERE sub=? AND utilisateur = ?;",(id,user))
                         elif est_participant(id,user):
                              cursor.execute("DELETE FROM participants WHERE sub=? AND utilisateur = ?;",(id,user))     
                         db.commit()
                         db.close()
                         return redirect(url_for('viewsub',id=id))
                    else :
                         return render_template('erreur.html',message="Impossible de se désabonner",description="Vous n'êtes pas abonné ou bien c'est votre projet")

               else :
                    return redirect('/')
          else:
               return render_template('erreur.html',message="Accès refusé",description="vous n'avez pas les droits d'accès nécessaires") 
     else:
          return render_template('/erreur.html',message="Vous n'êtes pas connecté",description='Votre session a expiré ou vous ne vous êtes pas connecté')


# Route liée au bouton Participer du projet n° 'id'
@app.route('/<id>/demande_participation')
def demande_participation(id):
     if test_login():
          if test_verif():
               if test_id_sub(id):
                    user = session.get('id')
                    if not a_demande(id,user) and not is_owner(id,user) and est_abonne(id,user):
                         db = sqlite3.connect('database.db')
                         cursor = db.cursor()
                         cursor.execute("INSERT INTO demande_participation(sub,utilisateur) VALUES (?,?)",(id,session.get('id')))
                         db.commit()
                         db.close()
                         return redirect(url_for('viewsub',id=id))
                    else:
                         return render_template('erreur.html',message="Impossible de demander à participer au projet",description="Vous n'êtes pas abonné ou bien c'est votre projet ou vous avez déjà fait une demande")

               else :
                    return redirect('/')
          else:
               return render_template('erreur.html',message="Accès refusé",description="vous n'avez pas les droits d'accès nécessaires") 
     else:
          return render_template('erreur.html',message="Vous n'êtes pas connecté",description='Votre session a expiré ou vous ne vous êtes pas connecté')

# Route liée au bouton Ne plus participer du projet n° 'id'
@app.route('/<id>/annuler_participation')
def annuler_participation(id):
     if test_login():
          if test_verif():
               if test_id_sub(id):
                    user = session.get('id')
                    if est_participant(id,user):
                         db = sqlite3.connect('database.db')
                         cursor = db.cursor()
                         cursor.execute("DELETE FROM participants WHERE sub=? AND utilisateur=?",(id,user))
                         db.commit()
                         db.close()
                         return redirect(url_for('viewsub',id=id))
                    else :
                         return render_template('erreur.html',message="Impossible d'annuler sa participation au projet",description="Vous ne participez pas au projet ou bien c'est votre projet")

               else :
                    return redirect('/')
          else:
               return render_template('erreur.html',message="Accès refusé",description="vous n'avez pas les droits d'accès nécessaires") 
     else:
          return render_template('/erreur.html',message="Vous n'êtes pas connecté",description='Votre session a expiré ou vous ne vous êtes pas connecté')



# Route liée à l'onglet Post du projet n° 'id'
@app.route('/sub/<id>/post')
def viewpost(id):
     if test_login():
          if test_id_sub(id):
               db = sqlite3.connect('database.db')
               cursor = db.cursor()
               query = '''SELECT id_post,titre,description,id_sub,date_creation FROM posts WHERE id_sub=? ORDER BY date_creation;'''
               cursor.execute(query,(id,))
               L =(cursor.fetchall(),id)
               comments={}
               for row in L[0]:
                    idpost=row[0]
                    cursor.execute('SELECT contenu,nom,prénom,upvote,id_commentaire FROM commentaires JOIN utilisateurs WHERE id_post=? AND posté_par=id_user' ,(idpost,))
                    données=cursor.fetchall()   
                    if données!=[]:
                         comments[idpost]=données
                         for i in range(len(données)):
                              données[i]+=(commentaire(données[i][4],str(session.get('id'))),) 
                    else:
                         comments[idpost]=[]
               db.close()
               user = session.get('id')
               abonne = est_abonne(id,user)
               owner = is_owner(id,user)
               participant = est_participant(id,user)
               return render_template('viewpost.html', data=L,comments=comments,id=id,abonne=abonne,owner=owner,participant=participant)
          else:
               return redirect('/')
     else:
          return render_template('/erreur.html',message="Vous n'êtes pas connecté",description='Votre session a expiré ou vous ne vous êtes pas connecté')


# Route liée au bouton Créer un nouveau post dans l'onglet Post du projet n° 'id'
@app.route('/sub/<id>/creationpost')
def newpost(id):
     if test_verif():
          if test_id_sub(id):
               user = session.get('id')
               if is_owner(id,user) or est_participant(id,user):
                    return render_template('newpost.html',data=id)
               else:
                    return render_template('erreur.html',message="Impossible de créer un post",description="Vous ne participez pas au projet ni n'êtes son créateur")        
          else:
               return redirect('/')
     else:
          return render_template('erreur.html',message="Accès refusé",description="vous n'avez pas les droits d'accès nécessaires") 
     

# Route liée au form pour créer un nouveau post lié au projet n° 'id'
@app.route('/postsub/<id>',methods = ['GET','POST'])
def postsub(id):
     if test_verif():
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
                              image.save(os.path.join(app.config["IMAGE_UPLOADS"], str(idpost[0][0])))
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
     else:
          return render_template('erreur.html',message="Accès refusé",description="vous n'avez pas les droits d'accès nécessaires") 
    
     

# Route liée au bouton Like sur un post d'id_post = 'id'
@app.route('/<id>/ajoutcompteur')
def updatecompteurpostpositif(id):
     if test_verif():
          db = sqlite3.connect('database.db')
          cursor = db.cursor()
          cursor.execute("SELECT id_sub FROM posts WHERE id_post= ?",(id,))
          id_sub = cursor.fetchall()[0][0]
          if test_id_sub(id_sub):
               cursor.execute("UPDATE posts SET ratio= ratio +1 WHERE id_post=?",(id,))
               db.commit()
               db.close()
               return redirect('/')
          else:
               db.close()
               return redirect('/')
     else:
          return render_template('erreur.html',message="Accès refusé",description="Vous n'avez pas les droits d'accès nécessaires") 


# Route liée au bouton Dislike du post d'id_post 'id'
@app.route('/<id>/retraitcompteur')
def updatecompteurpostnegatif(id):
     if test_verif():
          db = sqlite3.connect('database.db')
          cursor = db.cursor()
          cursor.execute("SELECT id_sub FROM posts WHERE id_post= ?",(id,))
          id_sub = cursor.fetchall()[0][0]
          if test_id_sub(id_sub):
               cursor.execute("UPDATE posts SET ratio= ratio -1 WHERE id_post=?",(id,))
               db.commit()
               db.close()
               return redirect('/')
          else:
               db.close()
               return redirect('/')
     else:
          return render_template('erreur.html',message="Accès refusé",description="vous n'avez pas les droits d'accès nécessaires") 
    

# Route liée à l'onglet Demande de participation du projet n° 'id'
@app.route('/sub/<id>/demandes')
def demande(id):
     if test_verif():
          if test_id_sub(id):
               if is_owner(id,session.get('id')):
                    db = sqlite3.connect('database.db')
                    cursor = db.cursor()
                    cursor.execute("SELECT utilisateur,nom,prénom FROM demande_participation JOIN utilisateurs WHERE id_user=utilisateur AND sub = ?",(id,))
                    data=cursor.fetchall()
                    db.close()
                    return render_template("participants.html",id=id,data=data)
               else :
                    return render_template('erreur.html',message="Accès refusé",description="Vous n'êtes pas le créateur du projet") 

          else:
               return redirect('/')
     else:
          return render_template('erreur.html',message="Accès refusé",description="Vous n'avez pas les droits d'accès nécessaires") 



# Route liée au bouton Accepter la participation de 'user' dans l'onglet Demande de participations du projet n° 'id'
@app.route('/<id>/accepter/<user>')
def accepter(id,user):
     if test_verif():
          db = sqlite3.connect('database.db')
          cursor = db.cursor()
          if test_id_sub(id):
               cursor.execute("INSERT INTO participants(sub,utilisateur) VALUES (?,?)",(id,user))
               cursor.execute("DELETE FROM demande_participation WHERE sub=? AND utilisateur=?",(id,user))
               db.commit()
               db.close()
               return redirect(url_for('demande',id=id))
          else:
               db.close()
               return redirect('/')
     else:
          return render_template('erreur.html',message="Accès refusé",description="vous n'avez pas les droits d'accès nécessaires") 
    

# Route liée au bouton Refuser la participation de 'user' dans l'onglet Demande de participations du projet n° 'id'
@app.route('/<id>/refuser/<user>')
def refuser(id,user):
     if test_verif():
          db = sqlite3.connect('database.db')
          cursor = db.cursor()
          if test_id_sub(id):
               cursor.execute("DELETE FROM demande_participation WHERE sub=? AND utilisateur=?",(id,user))
               db.commit()
               db.close()
               return redirect(url_for(demande,id=id))
          else:
               db.close()
               return redirect('/')
     else:
          return render_template('erreur.html',message="Accès refusé",description="vous n'avez pas les droits d'accès nécessaires") 
    

# Route liée à l'onglet Mon Profil
@app.route('/profil')
def voirleprofil():
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     if test_login():
          id_user = session.get('id')
          cursor.execute("SELECT niveau FROM utilisateurs WHERE id_user=?",(id_user,))
          niveau=cursor.fetchall()[0][0]
          cursor.execute("SELECT nom, prénom, mail, mdp FROM utilisateurs WHERE id_user=?",(id_user,))
          L= cursor.fetchall()
          db.close()
          mdp=L[0][3]
          mdp2=''
          for i in range(len(mdp)):
               mdp2+='*'
          if niveau=='A':
               return render_template('profil.html',data='e',L=L,mdp=mdp2)
          else:
               return render_template('profil.html',data=1,L=L,mdp=mdp2)
     else:
          db.close()
          return render_template('/erreur.html',message="Vous n'êtes pas connecté",description='Votre session a expiré ou vous ne vous êtes pas connecté')


# Route liée au bouton Gérer les accès des utilisateurs (accesible uniquement pour les adminastrateurs)
@app.route('/validation')
def validation_utilisateur():
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     if test_login():
          cursor.execute("SELECT niveau FROM utilisateurs WHERE id_user=?",(session.get("id"),))
          niveau=cursor.fetchall()[0][0]
          if niveau=='A':
               cursor.execute('SELECT niveau,id_user,nom,prénom FROM utilisateurs')
               data=cursor.fetchall()
               db.close()
               return render_template('validation.html',data=data)
          else:
               db.close()
               return render_template('erreur.html',message="Accès refusé",description="Vous n'avez pas les droits d'accès nécessaires") 
     else:
          db.close()
          return render_template('/erreur.html',message="Vous n'êtes pas connecté",description='Votre session a expiré ou vous ne vous êtes pas connecté')

     
# Route lié au bouton Mettre en 'niveau' l'utilisateur 'id' sur la page validation (pour gérer les niveaux des utilisateurs) 
@app.route('/<id>/<niveau>')
def update_niveau(id,niveau):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute("SELECT niveau FROM utilisateurs WHERE id_user=?",(id))
     niv=cursor.fetchall()
     cursor.execute("SELECT niveau FROM utilisateurs WHERE id_user=?",(session.get('id'),))
     user=cursor.fetchall()[0][0]
     if user=='A' and niv!=[]:
          if niveau=='Admin':
               cursor.execute("UPDATE utilisateurs SET niveau='A' WHERE id_user=?",(id,))
               db.commit()
               db.close()
               return redirect('/validation')
          elif niveau=='Validé':
               cursor.execute("UPDATE utilisateurs SET niveau='V' WHERE id_user=?",(id,))
               db.commit()
               db.close()
               return redirect('/validation')
          else:
               return redirect('/')
     else:
          db.close()
          return render_template('erreur.html',message="Accès refusé",description="Vous n'avez pas les droits d'accès nécessaires") 
    

# Route liée à l'ajout d'un commentaire sur le post      
@app.route('/comment/<id>',methods=['post'])
def post_commentaire(id):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     if test_login():
          if test_verif():
               content=request.form.to_dict()
               user=str(session.get("id"))
               if request.method=='POST':
                    cursor.execute('INSERT INTO commentaires(contenu,posté_par,id_post,likeur,upvote) VALUES (?,?,?,?,?)',(content['commentaire'],user,id,'/'+user,0))
                    db.commit()
               cursor.execute("SELECT id_sub FROM posts WHERE id_post = ?",(id,))
               id_sub = cursor.fetchall()[0][0]
               db.close()
               return redirect('/sub/'+str(id_sub)+'/post')
          else:
               db.close()
               return render_template('erreur.html',message="Accès refusé",description="vous n'avez pas les droits d'accès nécessaires") 
     else:
          db.close()
          return render_template('/erreur.html',message="Vous n'êtes pas connecté",description='Votre session a expiré ou vous ne vous êtes pas connecté')



@app.route('/mesabonnements')
def affichageabonnements():
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     if test_login():
          cursor.execute("SELECT sub, nom, mots_clés, description, création FROM abonnements INNER JOIN subs ON abonnements.sub=subs.numéro_projet WHERE utilisateur=?",(str(session.get("id"))))
          L=cursor.fetchall()
          db.close()
          return render_template('mesabonnements.html',data=L)
     else:
          db.close()
          return render_template('/erreur.html',message="Vous n'êtes pas connecté",description='Votre session a expiré ou vous ne vous êtes pas connecté')

'''@app.route('/mesabonnements')
def affichageabonnements():
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     cursor.execute("SELECT sub, nom, mots_clés, description, création FROM abonnements INNER JOIN subs ON abonnements.sub=subs.numéro_projet WHERE utilisateur=?",(str(session.get("id"))))
     L=cursor.fetchall()
     db.close()
     return render_template('mesabonnements.html',data=L)'''

@app.route('/mesprojets')
def affichageprojets():
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     if test_login():
          cursor.execute("SELECT numéro_projet, nom, mots_clés, description, création FROM subs WHERE créé_par=?",(str(session.get("id"))))
          L=cursor.fetchall()
          db.close()
          return render_template('mesprojets.html',data=L)
     else:
          db.close()
          return render_template('/erreur.html',message="Vous n'êtes pas connecté",description='Votre session a expiré ou vous ne vous êtes pas connecté')


@app.route('/upvote/<id_com>')
def upvote(id_com):
     db = sqlite3.connect('database.db')
     cursor = db.cursor()
     if test_login():
          if test_verif():
               cursor.execute("SELECT likeur FROM commentaires WHERE id_commentaire=?",(id_com,))
               likeur=cursor.fetchall()
               if str(session.get('id')) not in likeur[0][0].split('/'):
                    likeur=likeur[0][0]+'/'+str(session.get('id'))
                    cursor.execute("UPDATE commentaires SET upvote=upvote+1, likeur=? WHERE id_commentaire=?",(likeur,id_com))
                    db.commit()
               cursor.execute("SELECT id_sub FROM posts JOIN commentaires ON commentaires.id_post=posts.id_post WHERE commentaires.id_commentaire=?",(id_com,))
               id=cursor.fetchall()[0][0]
               db.close()
               return redirect('/sub/'+str(id)+'/post')
          else:
               db.close()
               return render_template('erreur.html',message="Accès refusé",description="vous n'avez pas les droits d'accès nécessaires") 
     else:
          db.close()
          return render_template('/erreur.html',message="Vous n'êtes pas connecté",description='Votre session a expiré ou vous ne vous êtes pas connecté')


@app.route("/sub/<numsub>/tchat", methods=["GET","POST"])
def chat(numsub):
     if test_login():
          if test_verif():
               user = session.get('id')
               if is_owner(numsub,user) or est_participant(numsub,user):
                    db = sqlite3.connect('database.db')
                    cursor = db.cursor()
                    id_posteur=session.get('id')
                    cursor.execute("""SELECT nom,prénom,message,date FROM chat JOIN utilisateurs WHERE numsub = ? AND id_user=id_posteur""",(numsub,))
                    data=cursor.fetchall()
                    if request.method=='POST':
                         now = time.localtime(time.time())
                         message = request.form['message']
                         cursor.execute("""
                         INSERT INTO chat(numsub,id_posteur,message,date) values(?,?,?,?)""",(numsub,id_posteur,str(message),time.strftime("%y/%m/%d %H:%M", now)))
                         db.commit()
                         db.close()
                    return render_template('chat.html',data=data,numsub=numsub)
               else :
                    return render_template('erreur.html',message="Accès refusé au chat",description="Vous n'êtes ni le créateur du projet ni un participant") 
    
          else:
               return render_template('erreur.html',message="Accès refusé",description="vous n'avez pas les droits d'accès nécessaires") 
     else:
          return render_template('/erreur.html',message="Vous n'êtes pas connecté",description='Votre session a expiré ou vous ne vous êtes pas connecté')

if __name__=='__main__':
     app.run(debug=1)
