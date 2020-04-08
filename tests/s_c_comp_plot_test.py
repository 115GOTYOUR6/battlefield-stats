# this allows an import from the parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from battlefield import plot
from pprint import pprint

rav = ['Turner SMLE', 'SEMI-AUTO RIFLE', '7,234', '1.52', '3d 07h 14m', '75,900', '23,189', '30.55', '1,815',
'Gewehr 1-5', 'SEMI-AUTO RIFLE', '4,631', '1.82', '1d 18h 24m', '63,699', '17,017', '26.71', '1,401',
'M1897', 'SHOTGUN', '2,907', '1.42', '1d 10h 01m', '9,391', '4,858', '51.73', '757',
'KE7', 'LMG', '2,385', '1.59', '1d 00h 56m', '46,418', '12,002', '25.86', '576',
'Jungle Carbine', 'BOLT ACTION CARBINE', '1,569', '1.21', '21h 36m 50s', '8,074', '2,995', '37.09', '989',
'Ag m/42', 'SEMI-AUTO RIFLE', '1,272', '1.35', '15h 40m 20s', '14,925', '5,085', '34.07', '451',
'M30 Drilling', 'SHOTGUN', '1,550', '1.70', '15h 10m 30s', '3,505', '6,115', '174.47', '254',
'Bren Gun', 'LMG', '1,316', '1.49', '14h 46m 20s', '24,143', '6,514', '26.98', '363',
'Lewis Gun', 'LMG', '896', '1.05', '14h 14m 40s', '21,304', '4,576', '21.48', '236',
'M1A1 Carbine', 'SEMI-AUTO RIFLE', '1,219', '1.45', '14h 01m 35s', '19,071', '5,149', '27.00', '458',
'Kar98k', 'BOLT ACTION RIFLE', '978', '1.20', '13h 38m 05s', '4,096', '1,544', '37.70', '763',
'M1 Garand', 'SEMI-AUTO RIFLE', '892', '1.23', '12h 05m 50s', '9,123', '3,045', '33.38', '249',
'12g Automatic', 'SHOTGUN', '1,228', '1.81', '11h 17m 40s', '3,990', '2,548', '63.86', '302',
'ZH-29', 'SELF-LOADING RIFLE', '1,027', '1.58', '10h 48m 55s', '5,508', '2,418', '43.90', '205',
'MAS 44', 'SEMI-AUTO RIFLE', '797', '1.54', '8h 36m 00s', '7,943', '2,500', '31.47', '255',
'Panzerfaust', 'GADGET', '384', '0.79', '8h 07m 50s', '3,088', '0', '0.00', '0',
'PIAT', 'GADGET', '518', '1.07', '8h 04m 40s', '2,806', '0', '0.00', '0',
'Krag–Jørgensen', 'BOLT ACTION RIFLE', '636', '1.33', '7h 57m 15s', '2,695', '999', '37.07', '514',
'Lee-Enfield No.4 Mk I', 'BOLT ACTION RIFLE', '585', '1.36', '7h 09m 20s', '2,541', '946', '37.23', '453',
'Ribeyrolles 1918', 'ASSAULT RIFLE', '601', '1.48', '6h 45m 50s', '11,382', '3,065', '26.93', '192',
'M1911', 'SIDEARM', '911', '2.25', '6h 44m 30s', '7,516', '2,512', '33.42', '158',
'Selbstlader 1906', 'SELF-LOADING RIFLE', '584', '1.51', '6h 26m 55s', '3,260', '1,354', '41.53', '120',
'Breda M1935 PG', 'ASSAULT RIFLE', '605', '1.59', '6h 21m 45s', '8,849', '2,544', '28.75', '152',
'MP40', 'SMG', '495', '1.40', '5h 53m 15s', '9,530', '2,416', '25.35', '90',
'Sturmgewehr 1-5', 'ASSAULT RIFLE', '446', '1.43', '5h 11m 30s', '9,349', '2,228', '23.83', '126',
'Selbstlader 1916', 'SEMI-AUTO RIFLE', '339', '1.13', '5h 00m 10s', '3,072', '1,047', '34.08', '92',
'Madsen MG', 'LMG', '612', '2.07', '4h 56m 10s', '11,885', '3,154', '26.54', '167',
'Sticky Dynamite', 'GADGET', '593', '2.11', '4h 41m 35s', '5,325', '0', '0.00', '0',
'ZK-383', 'SMG', '74', '0.32', '3h 51m 40s', '1,735', '340', '19.60', '21',
'StG 44', 'ASSAULT RIFLE', '324', '1.59', '3h 24m 05s', '6,483', '1,816', '28.01', '102',
'BAR M1918A2', 'LMG', '357', '1.92', '3h 06m 35s', '7,647', '2,199', '28.76', '123',
'Gewehr 43', 'SEMI-AUTO RIFLE', '193', '1.06', '3h 02m 20s', '1,874', '605', '32.28', '51',
'Ammo Crate', 'GADGET', '0', '0.00', '2h 37m 00s', '4,446', '0', '0.00', '0',
'Mk VI Revolver', 'SIDEARM', '210', '1.45', '2h 25m 00s', '1,069', '405', '37.89', '63',
'Model 27', 'SIDEARM', '168', '1.20', '2h 20m 55s', '650', '308', '47.38', '61',
'Type 2A', 'SMG', '227', '1.62', '2h 20m 20s', '7,820', '1,456', '18.62', '53',
'Katana', 'MELEE', '210', '1.60', '2h 11m 55s', '1,102', '210', '19.06', '0',
'Flare Gun', 'GADGET', '0', '0.00', '2h 11m 00s', '1,253', '0', '0.00', '0',
'AT Grenade Pistol', 'GADGET', '127', '0.98', '2h 10m 10s', '1,093', '0', '0.00', '0',
'M1922 MG', 'MMG', '118', '0.91', '2h 09m 05s', '4,746', '606', '12.77', '34',
'FG-42', 'LMG', '138', '1.09', '2h 07m 25s', '3,226', '767', '23.78', '30',
'Trench Carbine', 'PISTOL CARBINE', '204', '1.87', '1h 49m 00s', '3,224', '900', '27.92', '70',
'Type 11 LMG', 'LMG', '108', '1.08', '1h 40m 20s', '2,146', '546', '25.44', '37',
'Boys AT Rifle', 'ANTI-MATERIEL RIFLE', '76', '0.81', '1h 34m 30s', '352', '100', '28.41', '19',
'LS/26', 'LMG', '156', '1.68', '1h 33m 55s', '3,109', '813', '26.15', '47',
'Model 37', 'SHOTGUN', '153', '1.82', '1h 24m 50s', '440', '704', '160.00', '11',
'M2 Carbine', 'ASSAULT RIFLE', '97', '1.23', '1h 19m 10s', '2,784', '707', '25.40', '31',
'Type 99 Arisaka', 'BOLT ACTION RIFLE', '73', '1.01', '1h 12m 50s', '390', '126', '32.31', '50',
'M28 con Tromboncino', 'BOLT ACTION CARBINE', '54', '0.76', '1h 11m 30s', '313', '100', '31.95', '36',
'AT Mine', 'GADGET', '116', '1.93', '1h 00m 10s', '1,262', '0', '0.00', '0',
'Lunge Mine', 'GADGET', '67', '1.16', '58m 20s', '216', '0', '0.00', '0',
'Karabin 1938M', 'SEMI-AUTO RIFLE', '85', '1.55', '55m 50s', '809', '271', '33.50', '21',
'M1907 SF', 'ASSAULT RIFLE', '85', '1.60', '53m 35s', '1,467', '385', '26.24', '18',
'Gewehr M95/30', 'BOLT ACTION RIFLE', '75', '1.44', '52m 50s', '279', '108', '38.71', '56',
'STEN', 'SMG', '65', '1.33', '49m 40s', '1,217', '336', '27.61', '11',
'Ross Rifle Mk III', 'BOLT ACTION RIFLE', '51', '1.04', '49m 40s', '264', '85', '32.20', '37',
'Scout Knife M1916', 'MELEE', '7', '0.15', '48m 05s', '58', '22', '37.93', '0',
'Type 97 MG', 'LMG', '49', '1.04', '47m 00s', '1,316', '323', '24.54', '7',
'Smoke Grenade Rifle', 'GADGET', '0', '0.00', '45m 05s', '404', '0', '0.00', '0',
'Medical Syringe', 'GADGET', '0', '0.00', '42m 20s', '0', '0', '0.00', '0',
'M3 Grease Gun', 'SMG', '57', '1.54', '37m 45s', '1,040', '242', '23.27', '17',
'Spotting Scope', 'GADGET', '0', '0.00', '35m 25s', '84', '0', '0.00', '0',
'Selbstlader 1906', 'SELF-LOADING RIFLE', '51', '1.50', '34m 50s', '341', '124', '36.36', '13',
'MG 42', 'MMG', '27', '0.87', '31m 50s', '1,196', '156', '13.04', '2',
'Commando Carbine', 'BOLT ACTION CARBINE', '10', '0.40', '25m 05s', '93', '28', '30.11', '6',
'Bolo-Guna', 'MELEE', '20', '0.87', '23m 15s', '222', '30', '13.51', '0',
'P38 Pistol', 'SIDEARM', '46', '2.19', '21m 50s', '460', '147', '31.96', '7',
'M2 Flamethrower', 'GADGET', '21', '1.05', '20m 20s', '1,482', '0', '0.00', '0',
'Bandages', 'GADGET', '0', '0.00', '19m 15s', '2,117', '0', '0.00', '0',
'Incendiary Grenade', 'GADGET', '146', '9.12', '16m 20s', '1,395', '0', '0.00', '0',
'AP Mine', 'GADGET', '16', '1.33', '12m 55s', '219', '0', '0.00', '0',
'RSC', 'SELF-LOADING RIFLE', '22', '1.83', '12m 15s', '127', '51', '40.16', '5',
'Spawn Beacon', 'GADGET', '0', '0.00', '10m 40s', '176', '0', '0.00', '0',
'Cricket Bat', 'MELEE', '46', '4.60', '10m 15s', '698', '78', '11.17', '1',
'Fliegerfaust', 'GADGET', '1', '0.12', '08m 25s', '72', '0', '0.00', '0',
'M1928A1', 'SMG', '1', '0.14', '07m 40s', '75', '10', '13.33', '1',
'Medical Crate', 'GADGET', '0', '0.00', '07m 00s', '89', '0', '0.00', '0',
'Smoke Grenade', 'GADGET', '0', '0.00', '05m 50s', '547', '0', '0.00', '0',
'P08 Carbine', 'PISTOL CARBINE', '8', '1.60', '05m 05s', '175', '48', '27.43', '3',
'Frag Grenade Rifle', 'GADGET', '5', '1.25', '04m 15s', '29', '0', '0.00', '0',
'Kukri', 'MELEE', '43', '14.33', '03m 00s', '163', '62', '38.04', '0',
'Repetierpistole M1912', 'SIDEARM', '9', '4.50', '02m 50s', '103', '27', '26.21', '3',
'Sniper Decoy', 'GADGET', '0', '0.00', '02m 40s', '94', '0', '0.00', '0',
'Combat Knife', 'MELEE', '7', '7.00', '01m 55s', '247', '11', '4.45', '0',
'Frag Grenade', 'GADGET', '23', '23.00', '01m 50s', '211', '0', '0.00', '0',
'Suomi KP/-31', 'SMG', '1', '1.00', '01m 50s', '35', '6', '17.14', '1',
'MG 34', 'MMG', '1', '1.00', '01m 30s', '57', '11', '19.30', '0',
'Sticky Grenade', 'GADGET', '9', '9.00', '01m 20s', '115', '0', '0.00', '0',
'Kunai', 'GADGET', '0', '0.00', '01m 15s', '34', '0', '0.00', '0',
'Shovel', 'MELEE', '18', '18.00', '01m 15s', '68', '30', '44.12', '0',
'Barbed Baseball Bat', 'MELEE', '7', '7.00', '01m 05s', '58', '9', '15.52', '0',
'MKIII(S) Elite Combat Dagger', 'MELEE', '6', '6.00', '55s', '37', '11', '29.73', '0',
'P08 Pistol', 'SIDEARM', '1', '1.00', '55s', '9', '4', '44.44', '0',
'Fire Axe', 'MELEE', '2', '2.00', '40s', '36', '1', '2.78', '0',
'Anti-Tank Bundle Grenade', 'GADGET', '2', '2.00', '35s', '32', '0', '0.00', '0',
'Ruby', 'SIDEARM', '0', '0.00', '20s', '9', '2', '22.22', '0',
'Liberator', 'SIDEARM', '0', '0.00', '20s', '0', '0', '0.00', '0',
'The Unexpected Gift', 'MELEE', '4', '4.00', '20s', '29', '4', '13.79', '0',
'Okinawa Machete', 'MELEE', '1', '1.00', '15s', '13', '1', '7.69', '0',
'EGW Survival Knife', 'MELEE', '1', '1.00', '5s', '2', '2', '100.00', '0',
'MP28', 'SMG', '0', '0.00', '5s', '0', '0', '0.00', '0',
'Coupe Coupe', 'MELEE', '6', '6.00', '0s', '2', '1', '50.00', '0',
'EMP', 'SMG', '2', '2.00', '0s', '0', '0', '0.00', '0']

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

s_c_dict = plot.s_c_form(rav, "Ravic")
temp = plot.s_c_form(x, "115GOTYOUR6")
s_c_dict.update(temp)

plot.s_c_fillout(s_c_dict)

plot.s_c_comp_plot(s_c_dict, "./tests/s_c_plot_pics", stats2plot = ['accuracy'])
