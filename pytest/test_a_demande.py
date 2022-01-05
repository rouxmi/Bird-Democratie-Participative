import pytest
from app import a_demande

@pytest.mark.parametrize('id,user,attendu',[(24,1,True),(0,3,False),(6,0,False),(4,1,False)])

def test_a_demande(id,user,attendu):
    assert a_demande(id,user) == attendu