# File: battlefield_stats.py 
# Author: Jay Oliver
# Date Created: 11/03/2020
# Last Modified: 13/03/2020
# Purpose: This script is a data visualization tool for the stats
#          provided on the battlfield tracker website
# Comments:
#

import argparse
import requests
import sys

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

# the url is not expected to change so an option to specify it will not
# be provided
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
    raise Exception ("Unknown Error: page status "
                     "received was {}".format(page.status_code))
