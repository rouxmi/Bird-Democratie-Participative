import sqlite3
from flask.templating import render_template
import pytest
import datetime
import app

def connect(ses):
    ses.post('/connect',data={'username':'MICHEL.Louise@gmail.com','password':'qS8rb5l9guEB'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test:
        yield test

def contenu(id):
    subs = sqlite3.connect('database.db')
    cursor = subs.cursor()
    cursor.execute("""SELECT nom,mots_clés,description,création FROM subs where numéro_projet = ?""",(str(id),))
    contenu=cursor.fetchall()
    print(contenu)
    date=contenu[0][3].split('-')
    resultat=[]
    Y=int(date[0])
    M=int(date[1])
    D=int(date[2])

    resultat.append(contenu[0][:-1]+(str((datetime.date.today()-datetime.date(Y,M,D)).days)+' days ago',))
    return resultat

@pytest.mark.parametrize('search,expect',[('orn',''),('matin',contenu(28)),('oui',''),('racine haut',contenu(16)),('surprise pneu',contenu(12))])

def test_(base,search,expect):
    connect(base)
    response = base.post('/search',data={'Search':search})
    assert response.status_code == 200
    if type(expect)==type([]):
        for i in range(len(expect[0])):
            assert str(expect[0][i]).encode('UTF-8') in response.data
    else:
        assert expect.encode('UTF-8') in response.data
