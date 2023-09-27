import skysim_module


def test_make_stars_nsrc():

    ANDROMEDA_DEC = '00:42:44.3'
    ANDROMEDA_RA  = '41:16:09'

    NSRC = 1_000
    RADIUS = 1

    central_ra, central_dec = skysim_module.get_radec(ANDROMEDA_RA, ANDROMEDA_DEC)
    ras, decs = skysim_module.make_stars(central_ra, central_dec, NSRC, RADIUS)

    assert len(ras) == len(decs)
    assert NSRC == len(ras)

def test_make_stars_clip():
    ANDROMEDA_DEC = '00:42:44.3'
    ANDROMEDA_RA  = '41:16:09'

    NSRC = 1_000
    RADIUS = 1

    central_ra, central_dec = skysim_module.get_radec(ANDROMEDA_RA, ANDROMEDA_DEC)
    ras, decs = skysim_module.make_stars(central_ra, central_dec, NSRC, RADIUS)

    for (ira, idec) in zip(ras,decs):
        assert (ira - central_ra)**2 + (idec - central_dec)**2 < RADIUS**2
