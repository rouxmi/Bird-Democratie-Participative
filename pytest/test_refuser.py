import pytest
from app import refuser
import app

def connect(ses):
    ses.post('/connect',data={'username':'ROUX.Ambre@gmail.com','password':'iaCDoj06BXUp'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test_client:
        yield test_client

@pytest.mark.parametrize('id,user',[(18,14),(24,14),(0,14),(18,0),(None,15),(24,None),('ahgah','hfjhf')])

def test_(base,id,user):
    connect(base)
    response = base.get('/{id}/refuser/{user}')
    assert response.status_code == 302