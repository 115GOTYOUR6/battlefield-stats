# File: scrub.py 
# Author: Jay Oliver
# Date Created: 13/03/2020
# Last Modified: 27/03/2020
# Purpose: This file contains all functions that relate to web page
#          scrubbing
# Comments: More than one scrubbing fuction maybe created so as to
#           allow the scrubbing of different stats
#

from bs4 import BeautifulSoup
from re import search
from re import sub

from battlefield import time_played

def weaps(page):
    """Scrub and return the stats present on battlefield tracker webpage.


        This function scrubs the weapons page of
        battlefieldtracker.com for the stats on all the listed weapons
        and returns them in a dictionary.

        parameters:
            - page: This is the reasponse from the requests.get()
                    method which contains all the html of the site

        returns:
            - ret: This is a list with entries for each weapon stored
                   sequentially. It is structed as:
                   [weap_name, weap_class, kills, kpm, time,
                   shots_fired, shots_hit, shot_accuracy, headshots...
        raises:
            - valueError: This signifies that there is a stat with a value
                          is not of the type expected.
    """
    # these are entries that appear in the final parse (ret) that need
    # to be removed
    bad_ent = ["Search Profile", "Search", "Home", "My Profile",
               "Leaderboards", "Challenges", "More", "Link Profile",
               "Score/min", "K/D", "Rank", "Win %", "Kills",
               "Kills/min", "Time Played", "Shots Fired", "Shots Hit",
               "Shots Accuracy", "Headshots", "--"]

    soup = BeautifulSoup(page.content, "html.parser")
    parsed_soup = [str(i) for i in soup.find_all("span", ["name", "sub"])]
    ret = [search(r">.*<", i).group(0)[1:-1]
           for i
           in parsed_soup
           if search(r">.*<", i).group(0)[1:-1] not in bad_ent]

    # sanity check and format each of the results
    if(len(ret) % 9 != 0):
        raise ValueError("The number of entries in the scrubbed data was not a"
                         " multiple of 9. This may be the result of the"
                         " webpage changing its format or an unforseen entry"
                         " in a weapon stat field.")
    else:
        for i in range(int(len(ret)/9)):
            try:
                ret[i*9 + 2] = int(sub(",", "", ret[i*9 + 2])) # kills
                ret[i*9 + 3] = float(ret[i*9 + 3])             # kpm
                ret[i*9 + 4] = time_played.hours(ret[i*9 + 4]) # time played
                ret[i*9 + 5] = int(sub(",", "", ret[i*9 + 5])) # shots fired
                ret[i*9 + 6] = int(sub(",", "", ret[i*9 + 6])) # shots hit
                ret[i*9 + 7] = float(ret[i*9 + 7])             # accuracy
                ret[i*9 + 8] = int(sub(",", "", ret[i*9 + 8])) # headshots
            except ValueError:
                raise ValueError("One of the stats read in is not of the type"
                                 " expected.")
    # perhaps add a function call that puts the list into a dict?

    return ret
