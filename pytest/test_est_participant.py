import pytest
from app import est_participant

@pytest.mark.parametrize('id,user,expect',[(28,1,True),(2,1,False),('avk',3,False),(22,'?',False),(52,None,False),(19,22,False)])

def test_est_participant(id,user,expect):
    assert est_participant(id,user) == expect