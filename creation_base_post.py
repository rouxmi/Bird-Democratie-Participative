import sqlite3

query = '''
DROP TABLE if EXISTS post ;
CREATE TABLE post
(
    id_post INTEGER PRIMARY KEY AUTOINCREMENT,
    id_sub INTEGER FOREIGN KEY
    titre TEXT,
    description TEXT,
    date_deroulement DATE,
    nbre_visite INTEGER
);
'''
db = sqlite3.connect('liste_post.db')
cursor = db.cursor()
cursor.execute(query)
db.commit()
db.close()
