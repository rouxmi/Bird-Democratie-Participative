import pytest
import app

def connect(ses):
    ses.post('/connect',data={'username':'MICHEL.Louise@gmail.com','password':'qS8rb5l9guE'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test:
        yield test

@pytest.mark.parametrize('id',[(5),(43),(34),(32),(37),(25),(143),('z'),(132),(24)])
#cross check en regardant dans la BD
def test_abo(base,id):
    connect(base)
    response = base.get('/'+str(id)+'/abonnement')
    assert response.status_code == 302

