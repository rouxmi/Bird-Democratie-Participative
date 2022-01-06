import pytest
import app
import sqlite3


def connect(ses,username,mdp):
    ses.post('/connect',data={'username':username,'password':mdp},follow_redirects=True)

@pytest.fixture
def base():
    with app.app.test_client() as test:
        yield test

@pytest.mark.parametrize('username,mdp',[('MARTIN.LÃ©o@gmail.com', 'WB18j6jKYbvZ'), ('BERNARD.Gabriel@gmail.com', 'I4JCGERYKG5k'), ('THOMAS.RaphaÃ«l@gmail.com', 'l3IGIYYdAYLg'), ('PETIT.Arthur@gmail.com', 'EwzFnDmP3IBO'), ('ROBERT.Louis@gmail.com', 'xVGlY0PcIHc8'), ('RICHARD.Jules@gmail.com', 'QGhsEqJqhFaE'), ('DURAND.Adam@gmail.com', 'pnxy0eC5qVMz'), ('DUBOIS.MaÃ«l@gmail.com', '0iFAkzJlSOxv'), ('MOREAU.Lucas@gmail.com', 'Y6lWw3cPdJ40'), ('LAURENT.Hugo@gmail.com', 'zT0ilKIaQCMx'), ('SIMON.Jade@gmail.com', 'lgz0icWgmW5x'), ('MICHEL.Louise@gmail.com', 'qS8rb5l9guEB'), ('LEFEBVRE.Emma@gmail.com', 'CCKBkgHqQZrJ'), ('LEROY.Alice@gmail.com', 'aBA1JcJ4FePx'), ('ROUX.Ambre@gmail.com', 'iaCDoj06BXUp'), ('DAVID.Lina@gmail.com', 'pL1Whln4llH2'), ('BERTRAND.Rose@gmail.com', 'z1RKEGgiSFz5'), ('MOREL.ChloÃ©@gmail.com', 'ygQuYrHdfd46'), ('FOURNIER.Mia@gmail.com', 'pzIDY1H0Gdit'), ('GIRARD.LÃ©a@gmail.com', '8MoDUQC5wNuv'), ('coralie.serrand@telecomnancy.eu', 'ppiitncy'), ('bernard.dupont@gmail.com', 'bernarddupont'), ('durand.amanda@gmail.com', 'amandadurand'), ('Jean.Delafontaine@gmail.com', 'azerty12'), ('jean.valjean@gmail.com', 'azerty12'), ('alex.legrand@gmail.com', 'azerty12')])

#cross check en regardant dans la BD
def test_acceuil(base,username,mdp):
    connect(base,username,mdp)
    response = base.get('/')
    assert response.status_code == 302 or response.status_code == 200

