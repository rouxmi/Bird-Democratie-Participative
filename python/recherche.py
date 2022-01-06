import sqlite3

#prototype du nouvel algo de recherche
#fonctionne mais non implémenté
def liste_occurences(mots_recherches,L):
    nb_subs = len(L)
    subs = [0]*nb_subs
    ban_list=['de','du','le','la','les','un','une','des','je','tu','il','nous','vous','ils','elle','elles','on','au','aux','à','d','l']
    for i in range(nb_subs):
        sub = L[i]
        mots = []
        for j in range(3):
            mots = mots + sub[j].replace(' ',',').replace("'",",").split(',')
        occurence = 0
        for mot in mots:
            if mot not in ban_list:
                if mot in mots_recherches:
                    occurence += 1
        subs[i] = occurence
    return subs

def tri_decroissant(occurence,numéro_projet):
    max = 0
    for i in range(len(occurence)):
        if occurence[i]>max:
            numéro_projet


def recherche(s):
    mots_recherches = s.split()
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("SELECT nom,mots_clés,description FROM subs")
    L = cursor.fetchall()
    subs = liste_occurences(mots_recherches,L)
    print(subs)
    return subs


recherche("Compost écologique")