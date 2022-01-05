import pytest
import app

def connect(ses):
    ses.post('/connect',data={'username':'LEFEBVRE.Emma@gmail.com','password':'qS8rb5l9guE'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test:
        yield test

@pytest.mark.parametrize('id',[(7),(23),(54),(12),(17),(35),(43),(34),(42),(9)])
#cross check en regardant dans la BD
def test_upvote(base):
    connect(base)
    response = base.get('/upvote/'+str(id))
    assert response.status_code == 302 or response.status_code == 200

