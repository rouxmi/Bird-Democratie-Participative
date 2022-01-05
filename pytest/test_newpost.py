import pytest
from app import newpost
import app

def connect(ses):
    ses.post('/connect',data={'username':'ROUX.Ambre@gmail.com','password':'iaCDoj06BXUp'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test_client:
        yield test_client

@pytest.mark.parametrize('id',[24,35,6,0,None])

def test_(base,id):
    connect(base)
    response = base.get('/sub/{id}/creationpost')
    assert response.status_code == 302