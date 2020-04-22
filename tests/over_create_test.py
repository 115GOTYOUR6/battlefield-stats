# this allows an import from the parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from battlefield import overview
from pprint import pprint

x = ['Score/min', '485.82', 'K/D', '3.55', 'Rank', '61', 'Win %', '48.9%',
     'Score/min', '485.82', 'K/D', '3.55', 'Kills', '4,571', 'Kills/min',
     '1.27', 'Win %', '48.9%', 'Wins', '89', 'Deaths', '1,287', 'Assists',
     '1,001', 'Damage', '550,020', 'Heals', '12,652', 'Revives', '505',
     'Resupplies', '3,645', 'Support', 'Rank', '20', 'Score/min', '521.75',
     'K/D', '3.95', 'Kills/min', '1.40', 'Support', '20', '750,270',
     '521.75', '2,012', '1.40', '3.95', 'Assault', '20', '603,528', '466.04',
     '1,660', '1.28', '3.57', 'Medic', '17', '306,354', '454.53', '711',
     '1.05', '2.88', 'Recon', '8', '62,693', '482.25', '138', '1.06', '3.29',
     'Tanker', '0', '40,260', '694.14', '105', '1.81', '0.00', 'Pilot', '0',
     '0', '0.00', '0', '0.00', '0.00']

o_dict = overview.create(x, "115GOTYOUR6")

pprint(o_dict)
