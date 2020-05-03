# File: battlefield_stats.py
# Author: Jay Oliver
# Date Created: 11/03/2020
# Last Modified: 22/04/2020
# Purpose: This script is a data visualization tool for the stats
#          provided on the battlfield tracker website
# Comments:
#

from os.path import isdir
from os import mkdir
import argparse
import sys
import requests

from battlefield import scrub
from battlefield import weapons
from battlefield import overview
from battlefield import plot


OVER_STATS = ["assists", "damage", "deaths", "heals", "resupplies", "revives",
              "wins", "win %", "kills", "k/d", "kills/min", "score/min",
              "score", "rank"]
WEAP_STATS = ["kills", "kpm", "time played", "shots fired", "shots hit",
              "accuracy", "headshots", "hpk"]

parser = argparse.ArgumentParser(description="This is a program that"
                                             " provides a visual"
                                             " comparison of stats"
                                             " provided on"
                                             " battlefieldtracker.com")

parser.add_argument("page",
                    help="The page the stats are to be obtained from.",
                    type=str,
                    choices=["overview", "weapons"])

parser.add_argument("plotting",
                    help=("The way in which the stats will appear on the"
                          " figures. This can be singular, a single"
                          " profiles stats per figure or mult where all the"
                          " given profile stats appear on each figure. Note"
                          " that the latter mode only supports up to 4"
                          " profiles."),
                    type=str,
                    choices=["singular", "compare"])
parser.add_argument("dir",
                    help="The directory the figures will be saved to. Only"
                         " directories that require the creation of 1"
                         " folder will be accepted where the directory"
                         " currently doesn't exists",
                    type=str)


parser.add_argument("--weap_stats",
                    help="The weapon stats the user wants figures for. If"
                         " nothing is given all the stats retrieved will be"
                         " plotted",
                    type=str,
                    nargs='*',
                    choices=WEAP_STATS,
                    default=None)

parser.add_argument("--overview_stats",
                    help="The overview stats the user wants figures for. If"
                         " nothing is given all the stats retrieved will be"
                         " plotted",
                    type=str,
                    nargs='*',
                    choices=OVER_STATS,
                    default=None)

requiredNamed = parser.add_argument_group("required named arguments")

requiredNamed.add_argument("--platform",
                           help="The platform that the user account is on.",
                           type=str,
                           nargs='+',
                           choices=["origin", "xbl", "psn"],
                           required=True)

requiredNamed.add_argument("--prof_name",
                           help="The name of the battlefield account the"
                                " stats are for. NOTE to enter a name that"
                                " has space in it surround it with double"
                                " quotes.",
                           type=str,
                           nargs='+',
                           required=True)

args = parser.parse_args()

if len(args.prof_name) != len(args.platform):
    raise ValueError("The number of profiles specified does not match the"
                     " number of platforms specified, ensure that each profile"
                     " has the platform they are on given also!")
if (args.plotting == "compare" and len(args.prof_name) > 4
        or args.plotting == "compare" and len(args.prof_name) < 2):
    raise ValueError("The number of profiles provided is not supported for"
                     " compare mode, the range acceptable is 2-4")
if (args.page == "overview"
        and args.overview_stats is None
        and args.weap_stats is not None
        or args.page == "weapons"
        and args.overview_stats is not None
        and args.weap_stats is None):
    if args.overview_stats is None:
        flag = "weapons"
    else:
        flag = "overview"
    raise ValueError("Stats to plot were specified for {stat} with the plot"
                     " being for {plot}. This is likely a mistake. Please "
                     " ensure that you provide stats to plot for the same page"
                     " the stats are to be retreived"
                     " from".format(stat=flag, plot=args.page))

# REMOVE THIS WHEN SINGLE FIGURE PLOTTING IS ADDED FOR OVERVIEW STATS
if args.page == "overview" and args.plotting == "singular":
    raise ValueError("This has not been implemented yet!")

# this is required as the plt.save method in the plot module has been written
# to save the figure as dname/...
if args.dir[-1] == "/":
    args.dir = args.dir[:-1]
if not isdir(args.dir):
    print("The given directory doesn't exists do you want to create it?")
    opt = 'blabla'
    while opt not in ['y', 'n', 'q']:
        opt = input("y/n/q ")
    if opt in ('n', 'q'):
        print("exiting")
        sys.exit(1)
    if opt == 'y':
        try:
            mkdir(args.dir)
        except FileNotFoundError:
            raise ValueError("The directory specifeid requires the"
                             " creation of more than 1 folder, specify a"
                             " path that requires only 1 folder to be made")


urls = [("https://battlefieldtracker.com/bfv/profile/{plat}/{prof}"
         "/{page}".format(plat=args.platform[i], prof=args.prof_name[i],
                          page=args.page))
        for i in range(len(args.platform))]
# the url is not expected to change so an option to specify it will not
# be provided (its dice/EA we're taling bout here)
pages = []
for url in urls:
    try:
        page = requests.get(url)
    except requests.exceptions.HTTPError as errh:
        print("Http Error: {}".format(errh))
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print("Connection Error: {}".format(errc))
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print("Timeout: {}".format(errt))
        sys.exit(1)
    except requests.exceptions.TooManyRedirects as errr:
        print("Redirection Error: {}".format(errr))
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print("Uknown Error: {}".format(err))
        sys.exit(1)

    if page.status_code != 200:
        raise Exception("Unknown Error: page status received was {}"
                        .format(page.status_code))
    pages.append(page)

if args.page == "weapons":
    s_c_dict = {}
    for i in range(len(args.prof_name)):
        weapon_list = scrub.weaps(pages[i])
        temp = weapons.create(weapon_list, args.prof_name[i])
        s_c_dict.update(temp)
    # adding the hpk (heashots per kill) stat to the dict as this should be on
    # the battlefiled stats page to begin with
    weapons.add_hpk(s_c_dict)
    if args.plotting == "singular":
        plot.weap_plot(s_c_dict, args.dir, stats2plot=args.weap_stats,
                       up_buff=0.08)
    elif args.plotting == "compare":
        plot.weap_comp_plot(s_c_dict, args.dir, stats2plot=args.weap_stats,
                            up_buff=0.08)
    else:
        raise ValueError("A plotting class was not selected.")
else:
    over_dict = {}
    for i in range(len(args.prof_name)):
        over_list = scrub.overview(pages[i])
        temp = overview.create(over_list, args.prof_name[i])
        over_dict.update(temp)
    if args.plotting == "singular":
        pass
    elif args.plotting == "compare":
        plot.over_comp_plot(over_dict, args.dir,
                            stats2plot=args.overview_stats, up_buff=0.08)
    else:
        raise ValueError("A plotting class was not selected.")
