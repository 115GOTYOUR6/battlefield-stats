# File: scrub.py 
# Author: Jay Oliver
# Date Created: 13/03/2020
# Last Modified: 29/03/2020
# Purpose: This file contains all functions that relate to web page
#          scrubbing
# Comments: More than one scrubbing fuction maybe created so as to
#           allow the scrubbing of different stats
#           
#           The structure of the data that is parsed from the webpage (in the
#           data list) is:
#           Lewis Gun   # weapon name
#           LMG         # weapon class
#           737         # kills
#           1.48        # kpm
#           8h 19m 50s  # time played
#           21,624      # shots fired
#           4,260       # shots hit
#           19.70       # accuracy
#           169         # headshots
#           ...next weapon

from bs4 import BeautifulSoup
from re import search
from re import sub

from battlefield import time_played

def weaps(page, prof):
    """Scrub and return the stats present on battlefield tracker webpage.


        This function scrubs the weapons page of
        battlefieldtracker.com for the stats on all the listed weapons
        and returns them in a dictionary.

        parameters:
            - page: This is the response from the requests.get()
                        method which contains all the html of the site
            - prof: This is the name of the profile the stats are for as a
                        string

        returns:
            - stat_dict: this is a dictionary with all the stats in it. It has
                            the following key structure
                            |profile name
                            -|weapon class
                            --|weapon name
                            ---|stat (such as kills, kpm etc.)
                            ----|value
        raises:
            - valueError: This signifies that there is a stat with a value
                          is not of the type expected.
    """
    # these are entries that appear in the final parse (the data list) and need
    # to be removed
    bad_ent = ["Search Profile", "Search", "Home", "My Profile",
               "Leaderboards", "Challenges", "More", "Link Profile",
               "Score/min", "K/D", "Rank", "Win %", "Kills",
               "Kills/min", "Time Played", "Shots Fired", "Shots Hit",
               "Shots Accuracy", "Headshots", "--"]
    soup = BeautifulSoup(page.content, "html.parser")
    parsed_soup = [str(i) for i in soup.find_all("span", ["name", "sub"])]
    data = [search(r">.*<", i).group(0)[1:-1]
           for i
           in parsed_soup
           if search(r">.*<", i).group(0)[1:-1] not in bad_ent]

    stat_dict = {}
    stat_dict[prof] = {}

    if(len(data) % 9 != 0):
        raise ValueError("The number of entries in the scrubbed data was not a"
                         " multiple of 9. This may be the result of the"
                         " webpage changing its format or an unforseen entry"
                         " in a weapon stat field.")
    else:
        for i in range(int(len(data)/9)):
            w_class = data[i*9 + 1]
            w_name = data[i*9 + 0]
            if(w_class not in stat_dict[prof].keys()):
                stat_dict[prof][w_class] = {}
            stat_dict[prof][w_class][w_name] = {}
            try:
                stat_dict[prof][w_class][w_name]["kills"] = (
                    int(sub(",", "", data[i*9 + 2])))

                stat_dict[prof][w_class][w_name]["kpm"] = (
                    float(data[i*9 + 3]))

                stat_dict[prof][w_class][w_name]["time played"] = (
                    time_played.hours(data[i*9 + 4]))

                stat_dict[prof][w_class][w_name]["shots fired"] = (
                    int(sub(",", "", data[i*9 + 5])))

                stat_dict[prof][w_class][w_name]["shots hit"] = (
                    int(sub(",", "", data[i*9 + 6])))

                stat_dict[prof][w_class][w_name]["accuracy"] = (
                    float(data[i*9 + 7]))

                stat_dict[prof][w_class][w_name]["headshots"] = (
                    int(sub(",", "", data[i*9 + 8])))

            except ValueError:
                raise ValueError("One of the stats read in is not of the type"
                                 " expected.")

    return stat_dict
