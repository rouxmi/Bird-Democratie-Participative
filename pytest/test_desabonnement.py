import pytest
from app import desabonnement
import app

def connect(ses):
    ses.post('/connect',data={'username':'ROUX.Ambre@gmail.com','password':'iaCDoj06BXUp'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test_client:
        yield test_client


#cross check en regardant dans la BD
def test_(base):
    connect(base)
    response = base.get('/')
    assert response.status_code == 302