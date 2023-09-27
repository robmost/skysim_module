# Skysim - a first attempt at creating a synthtetic sky catalog

The initial requirements are as follows:

- Stars should have randomized sky positions around the Andromeda galaxy
- Positions should fall within 1 degree of the central location
- Each star should have a unique ID
- The star ID and position should be saved in a csv file to be analyzed by other programs

Usage: python sky_sim.py

Output: a file called 'catalog.csv' with the requested catalog as a CSV, and a plot of the distribution called
'skysim_distrib.png' as a PNG

Author: Robert Adriel Mostoghiu Paun

Developed at the 2023 ASA ECR Python workshop, University of Melbourne
