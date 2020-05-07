# File: scrub.py
# Author: Jay Oliver
# Date Created: 13/03/2020
# Last Modified: 21/04/2020
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
#           Note that this may not hold true if more stats are presented on
#           the webpage

from re import search
from bs4 import BeautifulSoup


def weaps(page):
    """Scrub and return the stats present on battlefield tracker webpage.


        This function scrubs the weapons page of
        battlefieldtracker.com for the stats on all the listed weapons
        and returns them in a list.

        parameters:
            - page: This is the response from the requests.get()
                        method which contains all the html of the site
        returns:
            - data: This is a list containing the stats for each weapon.
                        The order of the elements is given in the comment
                        of this file.
    """
    # these are entries that appear in the final parse (the data list) and need
    # to be removed
    bad_ent = ["Search Profile", "Search", "Home", "My Profile",
               "Leaderboards", "Challenges", "More", "Link Profile",
               "Score/min", "K/D", "Rank", "Win %", "Kills",
               "Kills/min", "Time Played", "Shots Fired", "Shots Hit",
               "Shots Accuracy", "Headshots", "--", "Premium"]
    soup = BeautifulSoup(page.content, "html.parser")
    parsed_soup = [str(i) for i in soup.find_all("span", ["name", "sub"])]
    data = [search(r">.*<", i).group(0)[1:-1]
            for i
            in parsed_soup
            if search(r">.*<", i).group(0)[1:-1] not in bad_ent]

    return data


def overview(page):
    """Scrub and return stats from the overview page on battlefield.tracker.com

    parameters:
        - page: This is the response from the requests.get()
                    method which contains all the html of the site
        - returns:
            - data: a list containing the parsed data from the html
    """
    bad_ent = ["Search Profile", "Search", "Home", "My Profile",
               "Leaderboards", "Challenges", "More", "Link Profile", "Premium"]
    soup = BeautifulSoup(page.content, "html.parser")
    parsed_soup = [str(i) for i in soup.find_all("span", ["name", "value",
                                                          "playtime"])]
    data = [search(r">.*<", i).group(0)[1:-1]
            for i
            in parsed_soup
            if search(r">.*<", i).group(0)[1:-1] not in bad_ent
            and "viewbox" not in search(r">.*<", i).group(0)[1:-1]]

    return data
