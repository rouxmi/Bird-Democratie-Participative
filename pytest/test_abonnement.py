import pytest
from app import abonnement
import app

def connect(ses):
    ses.post('/connect',data={'username':'MICHEL.Louise@gmail.com','password':'qS8rb5l9guEB'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test:
        yield test


#cross check en regardant dans la BD
def test_(base):
    connect(base)
    response = base.get('/')
    assert response.status_code == 302