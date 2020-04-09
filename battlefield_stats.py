# File: battlefield_stats.py 
# Author: Jay Oliver
# Date Created: 11/03/2020
# Last Modified: 9/04/2020
# Purpose: This script is a data visualization tool for the stats
#          provided on the battlfield tracker website
# Comments:
#

import argparse
import requests
import sys
from os.path import isdir
from os import mkdir

from battlefield import scrub
from battlefield import plot

parser = argparse.ArgumentParser(description="This is a script that"
                                             " provides a visual"
                                             " comparison of stats"
                                             " provided on"
                                             " battlefieldtracker.com"
                                )

parser.add_argument("plotting",
                    help = ("The way in which the stats will appear on the"
                            " figures. This can be singular, a single"
                            " profiles stats per figure or mult where all the"
                            " given profile stats appear on each figure. Note"
                            " that the latter mode only supports up to 4"
                            " profiles."
                           ),
                    type = str,
                    choices = ["singular", "compare"]
                   )
parser.add_argument("dir",
                    help = "The directory the figures will be saved to. Only"
                           " directories that require the creation of 1"
                           " folder will be accepted where the directory"
                           " currently doesn't exists",
                    type =str
                   )


parser.add_argument("--stats2plot",
                    help = "The stats that user wants figures for. If nothing"
                           " is given all the stats retrieved will be plotted",
                    type = str,
                    nargs = '*',
                    choices = ["kills", "kpm", "time played", "shots fired",
                               "shots hit", "accuracy", "headshots", "hpk"
                              ],
                    default = None
                   )


requiredNamed = parser.add_argument_group("required named arguments")

requiredNamed.add_argument("--platform",
                           help = "The platform that the user account is on.",
                           type = str,
                           nargs = '+',
                           choices=["origin", "xbox", "psn"],
                           required = True
                          )

requiredNamed.add_argument("--prof_name",
                           help = "The name of the battlefield account the"
                                  " stats are for. NOTE to enter a name that"
                                  " has space in it surround it with double"
                                  " quotes.",
                           type = str,
                           nargs = '+',
                           required = True
                          )

args = parser.parse_args()

if len(args.prof_name) != len(args.platform):
    raise ValueError("The number of profiles specified does not match the"
                     " number of platforms specified, ensure that each profile"
                     " has the platform they are on given also!"
                    )

if (args.plotting == "compare" and len(args.prof_name) > 4
    or args.plotting == "compare" and len(args.prof_name) < 2):
        raise ValueError("The number of profiles provided is not supported for"
                         " compare mode, the range acceptable is 2-4"
                        )


# this is required as the plt.save method in the plot module has been written
# to save the figure as dname/...
if args.dir[-1] == "/":
    args.dir = args.dir[:-1]
if not isdir(args.dir):
    print("The given directory doesn't exists do you want to create it?")
    opt = 'blabla'
    while opt not in ['y', 'n', 'q']:
        opt = input("y/n/q ")
    if opt == 'q' or opt == 'n':
        print("exiting")
        sys.exit(1)
    if opt == 'y':
        try:
            mkdir(args.dir)
        except FileNotFoundError:
            raise ValueError("The directory specifeid requires the"
                             " creation of more than 1 folder, specify a"
                             " path that requires only 1 folder to be made"
                            )


urls = [("https://battlefieldtracker.com/bfv/profile/{plat}/{prof}"
         "/weapons".format(plat = args.platform[i], prof = args.prof_name[i]))
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
        print ("Uknown Error: {}".format(err))
        sys.exit(1)

    if (page.status_code != 200):
        raise Exception ("Unknown Error: page status received was {}".format(page.status_code))
    pages.append(page)

s_c_dict = {}
for i in range(len(args.prof_name)):
    weapon_list = scrub.weaps(pages[i])
    temp = plot.s_c_form(weapon_list, args.prof_name[i])
    s_c_dict.update(temp)

# adding the hpk (heashots per kill) stat to the dict as this should be on
# the battlefiled stats page to begin with
plot.s_c_add_hpk(s_c_dict)
if args.plotting == "singular":
    plot.s_c_plot(s_c_dict, args.dir, stats2plot = args.stats2plot,
                  up_buff = 0.08
                 )
elif args.plotting == "compare":
    plot.s_c_comp_plot(s_c_dict, args.dir, stats2plot = args.stats2plot,
                  up_buff = 0.08
                 )
