# File: time_played.py
# Author: Jay Oliver
# Date Created: 24/03/2020
# Last Modified: 26/03/2020
# Pupose: Contains functions for manipulating a string that represents an
#         amount of time played
# Comments: The time played format is, xxd xxh xxm xxs where x is an integer.
#           The order of the time parameters is not considered important

def format(time):
    """Checks if the input parameter is a time played.

    parameters:
        - time: A string that is checked to have the time played format
    returns:
        - ret: A boolean represeting the conformaty of the input parameter
               time
    raises:
    """

    ret = -1
    temp = []
    try:
        temp = time.split(" ")
    except AttributeError:
        ret = False
    if(len([i[-1] for i in temp]) > 4 and ret == -1):
        ret = False
    elif(len(list(set([i[-1] for i in temp]))) != len(temp) and ret == -1):
        ret = False
    elif(ret == -1):
        for x in temp:
            # the implementation is casefold here makes the check non case
            # sensitive
            if(x[-1].casefold() not in ["d", "h", "m", "s"]):
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


def hours(time):
    """Convert a time played into a flaoting point number of hours.

    parameters:
        - time: The time played that will be converted into hours
    returns:
        - total: The time played converted
    raises:
    """

    if(format(time)):
        total = 0
        values = [int(i[:-1]) for i in time.split(" ")]
        mults = [i[-1] for i in time.split(" ")]
        for i in range(len(mults)):
            if(mults[i] == "d"):
                mults[i] = 24
            elif(mults[i] == "h"):
                mults[i] = 1
            elif(mults[i] == "m"):
                mults[i] = 1/60.0
            else:
                mults[i] = 1/60.0**2
        for i in range(len(values)):
            total = total + values[i] * mults[i]
    else:
        raise ValueError("The given parameter was not of the time played"
                         " format")
    return total
