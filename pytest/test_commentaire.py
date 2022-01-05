import pytest
from app import commentaire


@pytest.mark.parametrize('id_com,user,expect',[(11,5,(True,False)),(10,8,(False,True)),(34,3,(True,True)),('aaaeae',8,(True,True)),(13,10,(True,False))])

#cross check en regardant dans la BD
def test_is_owner(id_com,user,expect):
    assert commentaire(id_com,user) == expect