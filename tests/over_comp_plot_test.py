# this allows an import from the parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from battlefield import plot
from battlefield import overview
from pprint import pprint

over_dict = {'115GOTYOUR6': {'score/min': {'Career': 488.1, 'Support': 523.46, 'Assault': 470.28, 'Medic': 454.53, 'Recon': 482.25, 'Tanker': 731.74, 'Pilot': 0.0}, 'k/d': {'Career': 3.5, 'Support': 3.92, 'Assault': 3.57, 'Medic': 2.88, 'Recon': 3.29, 'Tanker': 0.0, 'Pilot': 0.0}, 'rank': {'Career': 62, 'Support': 20, 'Assault': 20, 'Medic': 17, 'Recon': 8, 'Tanker': 0, 'Pilot': 0}, 'win %': {'Career': 49.5}, 'kills': {'Career': 4780, 'Support': 2076, 'Assault': 1805, 'Medic': 711, 'Recon': 138, 'Tanker': 106, 'Pilot': 0}, 'kills/min': {'Career': 1.2, 'Support': 1.4, 'Assault': 1.28, 'Medic': 1.05, 'Recon': 1.06, 'Tanker': 1.83, 'Pilot': 0.0}, 'wins': {'Career': 95}, 'deaths': {'Career': 1346}, 'assists': {'Career': 1046}, 'damage': {'Career': 575175}, 'heals': {'Career': 12652}, 'revives': {'Career': 512}, 'resupplies': {'Career': 3735}, 'score': {'Support': 776287, 'Assault': 662151, 'Medic': 306354, 'Recon': 62693, 'Tanker': 42441, 'Pilot': 0}}}

rav = {'Ravic': {'score/min': {'Career': 625.9, 'Assault': 634.45, 'Support': 637.57, 'Recon': 583.05, 'Medic': 584.35, 'Tanker': 72549.57, 'Pilot': 9586.0}, 'k/d': {'Career': 4.7, 'Assault': 5.32, 'Support': 4.5, 'Recon': 4.39, 'Medic': 3.96, 'Tanker': 0.0, 'Pilot': 0.0}, 'rank': {'Career': 125, 'Assault': 20, 'Support': 20, 'Recon': 20, 'Medic': 20, 'Tanker': 0, 'Pilot': 0}, 'win %': {'Career': 81.3}, 'kills': {'Career': 46344, 'Assault': 23802, 'Support': 13706, 'Recon': 5017, 'Medic': 3756, 'Tanker': 901, 'Pilot': 16}, 'kills/min': {'Career': 1.5, 'Assault': 1.57, 'Support': 1.52, 'Recon': 1.36, 'Medic': 1.29, 'Tanker': 128.71, 'Pilot': 16.0}, 'wins': {'Career': 1319}, 'deaths': {'Career': 9667}, 'assists': {'Career': 8854}, 'damage': {'Career': 5096183}, 'heals': {'Career': 33636}, 'revives': {'Career': 3537}, 'resupplies': {'Career': 17443}, 'score': {'Assault': 9632149, 'Support': 5731087, 'Recon': 2154379, 'Medic': 1695792, 'Tanker': 507847, 'Pilot': 9586}}}

over_dict.update(rav)
pprint(over_dict)

plot.over_comp_plot(over_dict, "./tests/s_c_plot_pics", up_buff=0.08, stats2plot=["kills"])
