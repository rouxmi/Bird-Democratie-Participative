import pytest
from app import downlike
import app

def connect(ses):
    ses.post('/connect',data={'username':'LEFEBVRE.Emma@gmail.com','password':'CCKBkgHqQZrJ'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test:
        yield test

def test_(base):
    connect(base)
    response = base.get('/dislike/None')
    assert response.status_code == 302 or response.status_code == 200