import sqlite3

def createDB(id):
    nom_db = f"post_{id}"
    db = sqlite3.connect('post.db')
    cursor = db.cursor()
    args = (nom_db,)
    cursor.execute("CREATE TABLE %s(id_post INTEGER PRIMARY KEY AUTOINCREMENT, id_sub INTEGER, titre TEXT, description TEXT, date_creation DATE, nbr_visites INTEGER, FOREIGN KEY(id_sub) REFERENCES table1(Numéro_projet));" % nom_db) 
    db.commit()
    db.close()

if __name__== '__main__':
    createDB(2)

