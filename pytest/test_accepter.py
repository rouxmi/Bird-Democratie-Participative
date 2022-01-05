import pytest
import app

def connect(ses):
    ses.post('/connect',data={'username':'BERNARD.Gabriel@gmail.com','password':'I4JCGERYKG5k'},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test:
        yield test

@pytest.mark.parametrize('id,user',[('oui',15),(4,'ok'),(6,64),(7,32),(10,37),('oui','e'),(32,23),(16,74),(9,12),(42,19)])
#cross check en regardant dans la BD
def test_upvote(base,id,user):
    connect(base)
    response = base.get(str(id)+'/accepter/'+str(user))
    assert response.status_code == 302 or response.status_code == 200

