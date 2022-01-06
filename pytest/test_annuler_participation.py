import pytest
import sqlite3
from app import annuler_participation, session
import app

def connect(ses):
    ses.post('/connect',data={'username':'MARTIN.LÃ©o@gmail.com','password':'WB18j6jKYbvZ'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test:
        yield test

@pytest.mark.parametrize('id',[(25),(12),("a"),(4),(7),(56),(23),(None),('rt')])


def test_annuler_participation(base,id):
    connect(base)
    response = base.get()
    assert response.status_code == 200 or response.status_code == 302
    user = 1
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM participants WHERE sub=? AND utilisateur=?",(id,user))
    L=cursor.fetchall()
    db.commit()
    db.close()
    assert L==[]