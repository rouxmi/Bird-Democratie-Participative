import pytest
from app import demande
import app

def connect(ses):
    ses.post('/connect',data={'username':'PETIT.Arthur@gmail.com','password':'EwzFnDmP3IBO'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test:
        yield test

@pytest.mark.parametrize('id',[(18),(14),(0),(20),(None),('ahgah')])

def test_(base,id):
    connect(base)
    response = base.get('/comment/{id}')
    assert response.status_code == 302 or response.status_code == 200