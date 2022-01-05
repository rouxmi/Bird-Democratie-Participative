import pytest
from app import test_id_sub

@pytest.fixture()
def id():
    return

@pytest.mark.parametrize('id,expect',[(1,True),(330,False),(0,False),(None,False)])

def test_test_id_sub(id,expect):
    assert test_id_sub(id) == expect