# File: scrub.py 
# Author: Jay Oliver
# Date Created: 13/03/2020
# Last Modified: 16/03/2020
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
            - page:

        returns:
            - ret:

        raises:

    """

    soup = BeautifulSoup(page.content, 'html.parser')

    for x in str(soup.find_all("span", ["name", "sub"])).split(', '):
        print(x)
