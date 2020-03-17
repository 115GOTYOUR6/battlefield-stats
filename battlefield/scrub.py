# File: scrub.py 
# Author: Jay Oliver
# Date Created: 13/03/2020
# Last Modified: 17/03/2020
# Purpose: This file contains all functions that relate to web page
#          scrubbing
# Comments: More than one scrubbing fuction maybe createdso as to
#           allow the scrubbing of different stats
#

from bs4 import BeautifulSoup

def weaps(page):
    """
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

    """

    soup = BeautifulSoup(page.content, "html.parser")
    # this entry is one that will appear in the list that is parsed
    # from the soup and it needs to be removed.
    bad_ent = BeautifulSoup('<span class="sub" data-v-30f8f9f7="" data-v-7f5c8f78="">--</span>').span

    parsed_soup = [str(i) for i in soup.select('span[data-v-30f8f9f7=""]') if i != bad_ent]
    ret = [re.search(r">.*<", i).group(0)[1:-1] for i in parsed_soup]

    return ret
