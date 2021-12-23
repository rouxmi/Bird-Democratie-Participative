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

