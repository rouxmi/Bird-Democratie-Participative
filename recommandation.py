import sqlite3

def recommandation(id):
    subs = sqlite3.connect('database.db')
    cursor = subs.cursor()
    query='''SELECT Nom,Mots_clés FROM subs WHERE Numéro_projet=?'''
    cursor.execute(query,(id,))
    L=cursor.fetchall()
    query='''SELECT Numéro_projet,Nom,Mots_clés FROM subs WHERE NOT Numéro_projet=?'''
    cursor.execute(query,(id,))
    L2=cursor.fetchall()
    mots=L[0][1].replace(' ','').split(',')+L[0][0].replace(' ','').split(',')
    numero_projet=[]
    ban_list=['de','le','la','les','un','une','des','je','tu','il','nous','vous','ils','elle','elles','on','au','aux','à']
    for i in range(len(L2)):
        id=int(L2[i][0])
        comp=0
        temp=L2[i][1].replace(' ','').split(',')+L2[i][2].replace(' ','').split(',')
        for mot in mots:
            if mot not in ban_list:
                if mot in temp:
                    comp+=1
        numero_projet.append((id,comp))
    numero_projet.sort(key=lambda x:x[1],reverse=1)
    subs.close()
    return numero_projet
