import pytest
from app import desabonnement
import app

def connect(ses,username,mdp):
    ses.post('/connect',data={'username':username,'password':mdp},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test_client:
        yield test_client

@pytest.mark.parametrize('username,mdp,id',[('MARTIN.LÃ©o@gmail.com', 'WB18j6jKYbvZ',3), ('BERNARD.Gabriel@gmail.com', 'I4JCGERYKG5k',5), ('THOMAS.RaphaÃ«l@gmail.com', 'l3IGIYYdAYLg',12), ('PETIT.Arthur@gmail.com', 'EwzFnDmP3IBO',45), ('ROBERT.Louis@gmail.com', 'xVGlY0PcIHc8','a'), ('RICHARD.Jules@gmail.com', 'QGhsEqJqhFaE',23), ('DURAND.Adam@gmail.com', 'pnxy0eC5qVMz',None), ('DUBOIS.MaÃ«l@gmail.com', '0iFAkzJlSOxv','ok'), ('MOREAU.Lucas@gmail.com', 'Y6lWw3cPdJ40',18), ('LAURENT.Hugo@gmail.com', 'zT0ilKIaQCMx',23), ('SIMON.Jade@gmail.com', 'lgz0icWgmW5x',56), ('MICHEL.Louise@gmail.com', 'qS8rb5l9guEB',39), ('LEFEBVRE.Emma@gmail.com', 'CCKBkgHqQZrJ','oui'), ('LEROY.Alice@gmail.com', 'aBA1JcJ4FePx','ok'), ('ROUX.Ambre@gmail.com', 'iaCDoj06BXUp',345), ('DAVID.Lina@gmail.com', 'pL1Whln4llH2',None), ('BERTRAND.Rose@gmail.com', 'z1RKEGgiSFz5',53143), ('MOREL.ChloÃ©@gmail.com', 'ygQuYrHdfd46','gg'), ('FOURNIER.Mia@gmail.com', 'pzIDY1H0Gdit',69), ('GIRARD.LÃ©a@gmail.com', '8MoDUQC5wNuv',231), ('coralie.serrand@telecomnancy.eu', 'ppiitncy',90), ('bernard.dupont@gmail.com', 'bernarddupont',67), ('durand.amanda@gmail.com', 'amandadurand',76), ('Jean.Delafontaine@gmail.com', 'azerty12',841), ('jean.valjean@gmail.com', 'azerty12',98), ('alex.legrand@gmail.com', 'azerty12',8439)])


#cross check en regardant dans la BD
def test_(base,username,mdp,id):
    connect(base,username,mdp)
    response = base.get('/'+str(id)+'/desabonnement')
    assert response.status_code == 302 or response.status_code == 200