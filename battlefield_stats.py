# File: battlefield_stats.py 
# Author: Jay Oliver
# Date Created: 11/03/2020
# Last Modified: 12/03/2020
# Purpose: This script is a data visualization tool for the stats
#          provided on the battlfield tracker website
# Comments:
#

import argparse

parser = argparse.ArgumentParser(description="This is a script that "
                                             "provides a visual "
                                             "comparison of stats "
                                             "provided on "
                                             "battlefieldtracker.com")

parser.add_argument("platform",
                    help = "The platform that the user account is on.",
                    type = str,
                    choices=["origin", "xbox", "psn"])

parser.add_argument("prof_name", 
                    help = "the name of the battlefield account the "
                           "stats are for.", 
                    type = str,
                    nargs = '+')

args = parser.parse_args()

prof_name = " ".join(args.prof_name)

url = ("https://battlefieldtracker.com/bfv/profile/{plat}/{prof}"
       "/weapons".format(plat = args.platform, prof = prof_name))
