import pytest
from app import est_abonne

@pytest.mark.parametrize('id,user,expect',[(7,1,True),(33,3,False),(22,25,False),(37,None,False)])

def test_est_abonne(id,user,expect):
    assert est_abonne(id,user) == expect