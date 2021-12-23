import sqlite3

def createDB():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE posts (id_post INTEGER PRIMARY KEY AUTOINCREMENT, id_sub INTEGER, titre TEXT, description TEXT, posté_par INTEGER, date_creation DATE, ratio INTEGER, FOREIGN KEY(id_sub) REFERENCES subs(Numéro_projet));")
    db.commit()
    db.close()
createDB()