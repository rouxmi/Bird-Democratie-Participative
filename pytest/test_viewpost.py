import pytest
import app

def connect(ses):
    ses.post('/connect',data={'username':'DUBOIS.MaÃ«l@gmail.com','password':'0iFAkzJlSOxv'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test:
        yield test

@pytest.mark.parametrize('id',[(5),(43),(34),(32),(37),(25),(143),(434),(132),(24)])
#cross check en regardant dans la BD
def test_viewpost(base,id):
    connect(base)
    response = base.get('/sub/'+str(id)+'/post')
    assert response.status_code == 302 or response.status_code == 200

