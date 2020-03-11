# File: battlefield_stats.py 
# Author: Jay Oliver
# Date Created: 11/03/2020
# Last Modified: 11/03/2020
# Purpose: This script is a data visualization tool for the stats
#          provided on the battlfield tracker website
# Comments:
#

import argparse

parser = argparse.ArgumentParser(description="Process some integers.")

parser.add_argument('prof_name', 
                    help="the name of the battlefield account the "
                         "stats are for.", 
                    type=str,
                    nargs='+')

args = parser.parse_args()

prof_name = ' '.join(args.prof_name)
