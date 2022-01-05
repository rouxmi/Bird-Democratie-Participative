import pytest
from app import demande
import app

def connect(ses):
    ses.post('/connect',data={'username':'MICHEL.Louise@gmail.com','password':'qS8rb5l9guEB'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test:
        yield test

def test_(base):
    connect(base)
    response = base.get('/sub/153/chat')
    assert response.status_code == 302 or response.status_code == 200