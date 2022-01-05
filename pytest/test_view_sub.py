import pytest
from app import viewsub
import app

def connect(ses):
    ses.post('/connect',data={'username':'ROUX.Ambre@gmail.com','password':'iaCDoj06BXUp'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test:
        yield test

def test_(base):
    connect(base)
    response = base.get('/sub/19')
    assert response.status_code == 302 or response.status_code == 200