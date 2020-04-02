# this allows an import from the parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from battlefield import plot
from pprint import pprint
import argparse

parser = argparse.ArgumentParser(description="This is a test")

parser.add_argument("test",
                    help = "The scripts that need testing",
                    type = str,
                    choices = ["s_c_format", "s_c_plot"]
                   )
parser.add_argument("--stats2plot",
                    help = "The stats to plot",
                    type = str,
                    nargs = "*"
                   )

args = parser.parse_args()

x = ['Lewis Gun', 'LMG', '774', '1.49', '8h 41m 25s', '22,848', '4,478', '19.60',
 '174', 'StG 44', 'ASSAULT RIFLE', '751', '1.51', '8h 16m 10s', '21,171',
 '4,486', '21.19', '178', 'BAR M1918A2', 'LMG', '411', '1.49', '4h 35m 55s',
 '11,365', '2,738', '24.09', '102', 'M1 Garand', 'SEMI-AUTO RIFLE', '274',
 '1.08', '4h 14m 50s', '4,092', '1,186', '28.98', '57', 'Type 100', 'SMG',
 '205', '1.08', '3h 10m 55s', '6,466', '1,427', '22.07', '42', 'Turner SMLE',
 'SEMI-AUTO RIFLE', '196', '1.36', '2h 24m 50s', '2,759', '745', '27.00',
 '39', 'Sturmgewehr 1-5', 'ASSAULT RIFLE', '147', '1.29', '1h 54m 20s',
 '4,400', '1,089', '24.75', '24', 'EMP', 'SMG', '138', '1.29', '1h 47m 25s',
 '3,990', '794', '19.90', '24', 'Madsen MG', 'LMG', '111', '1.04',
 '1h 47m 20s', '3,103', '738', '23.78', '26', 'KE7', 'LMG', '100', '1.04',
 '1h 36m 35s', '3,152', '580', '18.40', '25', 'Type 2A', 'SMG', '127', '1.43',
 '1h 29m 40s', '4,915', '873', '17.76', '24', 'Ag m/42', 'SEMI-AUTO RIFLE',
 '82', '1.14', '1h 12m 00s', '1,153', '344', '29.84', '24',
 'Smoke Grenade Rifle', 'GADGET', '0', '0.00', '49m 10s', '424', '0', '0.00',
 '0', 'Mk VI Revolver', 'SIDEARM', '42', '0.89', '47m 30s', '341', '105',
 '30.79', '9', 'M1911', 'SIDEARM', '21', '0.48', '44m 35s', '395', '82',
 '20.76', '6', 'FG-42', 'LMG', '60', '1.40', '43m 00s', '1,539', '320',
 '20.79', '17', 'Selbstlader 1906', 'SELF-LOADING RIFLE', '44', '1.10',
 '40m 15s', '288', '105', '36.46', '4', 'PIAT', 'GADGET', '24', '0.63',
 '38m 20s', '278', '0', '0.00', '0', 'Fliegerfaust', 'GADGET', '11', '0.34',
 '32m 10s', '294', '0', '0.00', '0', 'Jungle Carbine', 'BOLT ACTION CARBINE',
 '17', '0.71', '24m 40s', '161', '37', '22.98', '5', 'MP28', 'SMG', '31',
 '1.29', '24m 30s', '951', '212', '22.29', '7', 'Type 97 MG', 'LMG', '29',
 '1.26', '23m 40s', '767', '132', '17.21', '15', 'Breda M1935 PG',
 'ASSAULT RIFLE', '22', '1.29', '17m 45s', '486', '119', '24.49', '2',
 'Suomi KP/-31', 'SMG', '19', '1.19', '16m 30s', '770', '116', '15.06', '3',
 'Sticky Dynamite', 'GADGET', '30', '2.00', '15m 50s', '364', '0', '0.00',
 '0', 'Ammo Crate', 'GADGET', '0', '0.00', '14m 50s', '679', '0', '0.00', '0',
 'Panzerfaust', 'GADGET', '0', '0.00', '14m 50s', '74', '0', '0.00', '0',
 'Model 8', 'SELF-LOADING RIFLE', '22', '1.57', '14m 45s', '172', '54',
 '31.40', '3', 'P38 Pistol', 'SIDEARM', '15', '1.15', '13m 35s', '278', '65',
 '23.38', '4', 'Medical Syringe', 'GADGET', '0', '0.00', '13m 20s', '0', '0',
 '0.00', '0', 'P08 Carbine', 'PISTOL CARBINE', '23', '1.77', '13m 15s', '476',
 '132', '27.73', '4', 'AT Mine', 'GADGET', '12', '1.00', '12m 15s', '360',
 '0', '0.00', '0', 'M1919A6', 'MMG', '6', '0.67', '09m 30s', '397', '37',
 '9.32', '2', 'Lee-Enfield No.4 Mk I', 'BOLT ACTION RIFLE', '1', '0.12',
 '08m 25s', '32', '7', '21.88', '1', 'Type 99 Arisaka', 'BOLT ACTION RIFLE',
 '3', '0.43', '07m 50s', '32', '8', '25.00', '3', '12g Automatic', 'SHOTGUN',
 '10', '1.67', '06m 20s', '46', '53', '115.22', '1', 'Bandages', 'GADGET',
 '0', '0.00', '05m 40s', '845', '0', '0.00', '0', 'Ribeyrolles 1918',
 'ASSAULT RIFLE', '9', '1.80', '05m 25s', '174', '38', '21.84', '1',
 'Spotting Scope', 'GADGET', '0', '0.00', '04m 45s', '23', '0', '0.00', '0',
 'LS/26', 'LMG', '3', '0.75', '04m 15s', '110', '15', '13.64', '0',
 'Flare Gun', 'GADGET', '0', '0.00', '04m 00s', '40', '0', '0.00', '0',
 'M2 Carbine', 'ASSAULT RIFLE', '0', '0.00', '03m 55s', '137', '21', '15.33',
 '0', 'Smoke Grenade', 'GADGET', '0', '0.00', '03m 45s', '293', '0', '0.00',
 '0', 'ZK-383', 'SMG', '1', '0.50', '02m 30s', '31', '7', '22.58', '1',
 'Model 27', 'SIDEARM', '3', '1.50', '02m 30s', '15', '4', '26.67', '1',
 "Solveig's Knife", 'MELEE', '1', '0.50', '02m 25s', '104', '1', '0.96', '0',
 'MAS 44', 'SEMI-AUTO RIFLE', '0', '0.00', '02m 15s', '40', '6', '15.00', '0',
'MP40', 'SMG', '3', '1.50', '02m 05s', '76', '10', '13.16', '1', 'M1928A1',
'SMG', '0', '0.00', '01m 45s', '41', '5', '12.20', '0', 'STEN', 'SMG', '0',
'0.00', '01m 15s', '5', '0', '0.00', '0', 'Gewehr 43', 'SEMI-AUTO RIFLE', '4',
'4.00', '01m 10s', '29', '14', '48.28', '1', 'AP Mine', 'GADGET', '1', '1.00',
'01m 10s', '33', '0', '0.00', '0', 'VGO', 'MMG', '1', '1.00', '01m 10s', '12',
'3', '25.00', '0', 'M30 Drilling', 'SHOTGUN', '0', '0.00', '55s', '4', '4',
'100.00', '0', 'ZH-29', 'SELF-LOADING RIFLE', '0', '0.00', '55s', '6', '1',
'16.67', '0', 'Frag Grenade', 'GADGET', '1', '1.00', '50s', '57', '0', '0.00',
'0', 'Spawn Beacon', 'GADGET', '0', '0.00', '45s', '26', '0', '0.00', '0',
'Anti-Tank Bundle Grenade', 'GADGET', '14', '14.00', '45s', '97', '0', '0.00',
'0', 'Impact Grenade', 'GADGET', '5', '5.00', '40s', '42', '0', '0.00', '0',
'EGW Survival Knife', 'MELEE', '1', '1.00', '30s', '22', '1', '4.55', '0',
'Sticky Grenade', 'GADGET', '0', '0.00', '30s', '27', '0', '0.00', '0',
'Bren Gun', 'LMG', '0', '0.00', '25s', '9', '3', '33.33', '0',
'M2 Flamethrower', 'GADGET', '1', '1.00', '25s', '128', '0', '0.00', '0',
'Incendiary Grenade', 'GADGET', '2', '2.00', '20s', '20', '0', '0.00', '0',
'Katana', 'MELEE', '0', '0.00', '15s', '0', '0', '0.00', '0',
'Scout Knife M1916', 'MELEE', '0', '0.00', '10s', '16', '0', '0.00', '0',
'Lunge Mine', 'GADGET', '0', '0.00', '10s', '0', '0', '0.00', '0']

s_c_dict = plot.s_c_form(x, "115GOTYOUR6")
if args.test == "s_c_format":
    pprint(s_c_dict)

elif args.test == "s_c_plot":
    plot.s_c_plot(s_c_dict, "./tests/s_c_plot_pics", args.stats2plot)
