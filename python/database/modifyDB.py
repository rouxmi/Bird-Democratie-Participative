import sqlite3
from createDB import *


db = sqlite3.connect('database.db')
cursor = db.cursor()
cursor.executescript("")
db.commit()
db.close()

createDBcommentaires()