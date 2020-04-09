import argparse
from os import mkdir
from os.path import isdir
import sys

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
                    help = "The directory the figures will be saved to",
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
                                  " stats are for. NOTE to enter a name that has"
                                  " space in it surround it with double quotes.",
                           type = str,
                           nargs = '+',
                           required = True
                          )

args = parser.parse_args()

urls = [("https://battlefieldtracker.com/bfv/profile/{plat}/{prof}"
         "/weapons".format(plat = args.platform[i], prof = args.prof_name[i]))
       for i in range(len(args.platform))]

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

print(args.stats2plot)

#print(args.platform)
#print(args.prof_name)
#print(urls)
