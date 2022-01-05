import pytest
from app import downlike
import app

def connect(ses):
    ses.post('/connect',data={'username':'LEFEBVRE.Emma@gmail.com','password':'CCKBkgHqQZrJ'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test:
        yield test

@pytest.mark.parametrize('id',[(18),(14),(0),(20),(None),('ahgah')])

def test_(base,id):
    connect(base)
    response = base.get('/dislike/{id}')
    assert response.status_code == 302 or response.status_code == 200