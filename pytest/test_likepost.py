import pytest
from app import likepost

@pytest.mark.parametrize('id_post,user,expect',[(0,1,(True,True)),(1,0,(True,True)),(2,10,(True,False)),(4,3,(False,True))])

def test_likepost(id_post,user,expect):
    assert likepost(id_post,user) == expect