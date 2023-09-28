#! /Users/rmostoghiupaun/anaconda3/bin/ python
'''
Simulate a catalog of stars near to the Andromeda constellation
'''

# Determine Andromeda location in RA/DEC degrees
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import logging

BASEPATH = '/Users/rmostoghiupaun/2023-ASA-ECR-Python/day1/skysim_module/data/'

# configure logging
logging.basicConfig(format="%(name)s:%(levelname)s %(message)s", level=logging.INFO)
mylogger = logging.getLogger("sky_sim")


def get_radec(ref_ra: str, ref_dec: str) -> list:
    """
    get_radec obtain the right ascension and declination coordinates from a string

    Args:
        ref_ra (str): RA in string format of the target galaxy
        ref_dec (str): DEC in string format of the target galaxy

    Returns:
        list: list containg the RA, DEC of Andromeda
    """
    if mylogger.isEnabledFor(logging.DEBUG):
        mylogger.debug("Fetching reference coordinates")

    REF_RA  = ref_ra
    REF_DEC = ref_dec

    degrees, minutes, seconds = REF_DEC.split(':')
    dec = int(degrees)+int(minutes)/60+float(seconds)/3600

    if mylogger.isEnabledFor(logging.DEBUG):
        mylogger.debug(f"DEC is: {degrees} deg, {minutes} min, {seconds} sec -> {dec} degrees")

    hours, minutes, seconds = REF_RA.split(':')
    ra = 15*(int(hours)+int(minutes)/60+float(seconds)/3600)
    ra = ra/np.cos(dec*np.pi/180)

    if mylogger.isEnabledFor(logging.DEBUG):
        mylogger.debug(f"RA is: {hours} hrs, {minutes} min, {seconds} sec -> {ra} degrees")

    return ra, dec

def clip_to_radius(ras: list, decs: list, ref_ra: float, ref_dec: float, radius: float) -> list:
    """
    clip_to_radius ensures the positions fit within a given radius

    Args:
        ras (list): list with right ascensions
        decs (list): list with declinations
        ref_ra (float): reference right ascension
        ref_dec (float): reference declination
        radius (float): radius to clip in respect of

    Returns:
        list: clipped right ascensions and declinations
    """

    if mylogger.isEnabledFor(logging.DEBUG):
        mylogger.debug(f"Clipping the positions to a radius of value {radius}")

    ra_out = []
    dec_out = []

    # ensure they have the same length
    assert len(ras) == len(decs)

    for i in range(len(ras)):
        if (ras[i]-ref_ra)**2 + (decs[i]-ref_dec)**2 < radius**2:
            ra_out.append(ras[i])
            dec_out.append(decs[i])

    if mylogger.isEnabledFor(logging.DEBUG):
        mylogger.debug(f"Positions clipped")

    return ra_out, dec_out


def make_stars(ref_ra: float, ref_dec: float, nsrc: int, radius: float) -> list:
    """
    make_stars return a list of RAs and DECs containg random

    Args:
        ref_ra (float): RA of reference galaxy
        ref_dec (float): DEC of reference galaxy
        nsrc (int): number of sources to generate
        radius (float): radius to clip the stars to

    Returns:
        list: list containing random RAs and DECs
    """

    if mylogger.isEnabledFor(logging.DEBUG):
        mylogger.debug(f"Generating synthetic star positions")

    ras = []
    decs = []
    for _ in range(nsrc):
        ras.append(ref_ra + random.uniform(-1, 1))
        decs.append(ref_dec + random.uniform(-1, 1))

    # apply our filter
    ras, decs = clip_to_radius(ras,decs,ref_ra,ref_dec,radius)

    if mylogger.isEnabledFor(logging.DEBUG):
        mylogger.debug(f"Synthetic star positions created")

    return ras, decs

def save_positions_to_file(ras: list, decs: list):
    """
    save_positions_to_file save the list of RAs and DECs as a csv file

    Args:
        ras (list): list containing the RAs of the galaxy
        decs (list): list containing the DECs of the galaxy
    """

    # now write these to a csv file for use by my other program

    if mylogger.isEnabledFor(logging.DEBUG):
        mylogger.debug(f"Writing synthetic star positions to a catalog")

    with open(BASEPATH + 'catalog.csv','w', encoding="utf8") as file:
        print('id,RA,DEC', file=file)

        # ensure they have the same length
        assert len(ras) == len(decs)

        for i in range(len(ras)):
            print(f"{i:07d},{ras[i]:12f},{decs[i]:12f}", file=file)

    if mylogger.isEnabledFor(logging.DEBUG):
        mylogger.debug(f"Catalog written")

def skysim_parser():
    """
    skysim_parser configure the argparse for skysim

    Returns:
        ArgumentParser: the parser of the module
    """
    parser = argparse.ArgumentParser(prog='sky_sim', prefix_chars='-')

    parser.add_argument('--ra', dest = 'ra', type=float, default=None,
                        help="Central ra (degrees) for the simulation location")
    parser.add_argument('--dec', dest = 'dec', type=float, default=None,
                        help="Central dec (degrees) for the simulation location")
    parser.add_argument('--out', dest='out', type=str, default=BASEPATH + 'catalog.csv',
                        help='destination for the output catalog')
    # parser.add_argument('--log-level', dest='log_level', type=str, default='INFO',
    #                     help='log level for logging. Available levels: DEBUG, INFO, WARNING, ERROR, CRITICAL')
    return parser



if __name__ == "__main__":

    NSRC     = 1_000
    RADIUS   = 1

    # from wikipedia
    ANDROMEDA_DEC = '00:42:44.3'
    ANDROMEDA_RA = '41:16:09'

    parser = skysim_parser()
    options = parser.parse_args()

    if None in [options.ra, options.dec]:
        central_ra, central_dec = get_radec(ANDROMEDA_DEC, ANDROMEDA_RA)
    else:
        central_ra = options.ra
        central_dec = options.dec

    # if None in options.log_level or ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] not in options.log_level:
    #     logging.basicConfig(logging.INFO)
    # else:
    #     logging.basicConfig(logging.log_level)

    ras, decs = make_stars(central_ra, central_dec, NSRC, RADIUS)

    assert len(ras) == len(decs)

    # now write these to a csv file for use by my other program
    with open(options.out, 'w') as f:
        print("id,ra,dec", file=f)

        for i in range(len(ras)):
            print(f"{i:07d}, {ras[i]:12f}, {decs[i]:12f}", file=f)

    mylogger.info(f"Wrote {options.out}")

    # plot it
    starcatalog = pd.read_csv(BASEPATH + 'catalog.csv', sep=",")

    plt.figure(figsize=(4,4), dpi=200)
    plt.plot(starcatalog['ra'], starcatalog['dec'], marker='.', markersize=3, ls='none')
    plt.xlabel('RA')
    plt.ylabel('DEC')
    plt.tight_layout()
    plt.savefig(BASEPATH + 'skysim_distrib.png')
    mylogger.info("Plotted the distribution")
