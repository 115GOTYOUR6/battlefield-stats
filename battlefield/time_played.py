# File: time_played.py
# Author: Jay Oliver
# Date Created: 24/03/2020
# Last Modified: 
# Pupose: Contains functions for manipulating a string that represents an
#         amount of time played
# Comments: The time played format is, xxh xxm xxs where x is an integer
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# This is incomplete, the format funtion returns a false positive for a string
# like xxh xxs xxs

def format(time):
    """Checks if the input parameter is a time played.

    parameters:
        - time: A string that is checked to have the time played format
    returns:
        - ret: A boolean represeting the conformaty of the input parameter
               time
    raises:
    """

    try:
        temp = time.split(" ")
    except AttributeError:
        raise ValueError("The input parameter could not be split.")

    for x in temp:
        # the implementation is casefold here makes the check non case
        # sensitive
        print(x[-1].casefold())
        if(x[-1].casefold() not in ["h", "m", "s"]):
            ret = False
            break
        else:
            try:
                int(x[:-1])
                ret = True
            except ValueError:
                ret = False
                break

    return ret
