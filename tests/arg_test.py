import argparse
from os import mkdir
from os.path import isdir
import sys

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

print(urls)

#print(args.platform)
#print(args.prof_name)
#print(urls)
