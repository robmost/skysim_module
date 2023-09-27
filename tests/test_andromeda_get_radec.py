import numpy as np
import skysim_module

def test_adromeda_get_radec():
    ANDROMEDA_DEC = '00:42:44.3'
    ANDROMEDA_RA  = '41:16:09'

    central_ra, central_dec = skysim_module.get_radec(ANDROMEDA_RA, ANDROMEDA_DEC)

    eps = 1e-10

    assert np.abs(central_ra - 14.215420962967535) < eps
    assert np.abs(central_dec - 41.269166666666667) < eps

    return