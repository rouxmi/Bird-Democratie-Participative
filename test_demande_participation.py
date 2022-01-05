import pytest
from app import demande
import app
import sqlite3

def connect(ses):
    ses.post('/connect',data={'username':'MICHEL.Louise@gmail.com','password':'qS8rb5l9guEB'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test:
        yield test

@pytest.mark.parametrize('id',[(1),(2)])

def test_demande_participation(base,id):
    connect(base)
    base.get('/{id}/demande_participation')
    db=sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM demande_participation WHERE sub=? AND utilisateur=12",(id,))
    data=cursor.fetchall()
    db.close()
    assert data != []
