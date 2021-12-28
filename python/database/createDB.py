import sqlite3

def createDBposts():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE posts (id_post INTEGER PRIMARY KEY AUTOINCREMENT, id_sub INTEGER, titre TEXT, description TEXT, posté_par INTEGER, date_creation DATE, ratio INTEGER, FOREIGN KEY(id_sub) REFERENCES subs(Numéro_projet));")
    db.commit()
    db.close()


def createDBabonnements():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE abonnements (sub INTEGER NOT NULL,utilisateur INTEGER NOT NULL, PRIMARY KEY(sub,utilisateur),FOREIGN KEY(sub) REFERENCES subs(numéro_projet),FOREIGN KEY(utilisateur) REFERENCES utilisateurs(id_user));")
    db.commit()
    db.close()

def createDBparticipants():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE participants(sub INTEGER NOT NULL,utilisateur INTEGER NOT NULL, PRIMARY KEY(sub,utilisateur),FOREIGN KEY(sub) REFERENCES subs(numéro_projet),FOREIGN KEY(utilisateur) REFERENCES utilisateurs(id_user));")
    db.commit()
    db.close()

def createDBdemandeparticipation():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE demande_participation(sub INTEGER NOT NULL,utilisateur INTEGER NOT NULL, PRIMARY KEY(sub,utilisateur),FOREIGN KEY(sub) REFERENCES subs(numéro_projet),FOREIGN KEY(utilisateur) REFERENCES utilisateurs(id_user));")
    db.commit()
    db.close()


def createDBsubs():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE subs(nom TEXT, créé_par INTEGER, numéro_projet INTEGER PRIMARY KEY AUTOINCREMENT, mots_clés TEXT, description TEXT, création DATE,FOREIGN KEY(créé_par) REFERENCES utilisateurs(id_user));")
    db.commit()
    db.close()

def createDButilisateurs():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE utilisateurs(id_user INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prénom TEXT,niveau VARCHAR(1), mail TEXT, mdp TEXT) ")
    db.commit()
    db.close()


def createDBcommentaires():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE commentaires(id_comment INTEGER PRIMARY KEY AUTOINCREMENT, contenu TEXT,posté_par INTEGER,id_post INTEGER) ")
    db.commit()
    db.close()

def createDBtchat():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE tchat(id INTEGER PRIMARY KEY AUTOINCREMENT,numsub INTEGER,idpostant INTEGER,message TEXT,date DATETIME) ")
    db.commit()
    db.close()