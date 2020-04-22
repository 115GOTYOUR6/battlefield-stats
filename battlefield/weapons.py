# File: weapons.py
# Author: Jay Oliver
# Date Created: 22/04/2020
# Date Last Modified: 22/04/2020
# Purpose: Contains all methods that create and manipulate weapon stat
#          dictionaries
#
# Comments: If the number of stats presented on the battlefield tracker
#           website changes the methods in this module will break. I have
#           chosen not to support any new additions as it is unlikely to
#           get any since its bfv
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
#
#           s_c_dict or stats class dictionary format is:
#           |prof
#           -|stat
#           --|weapon class
#           ---|weapon name
#           ----|value

from re import sub

from battlefield import time_played


def create(data, prof):
    """The ouput of the scrub method is converted into a dictionary.

    The intended format of the dictionary returned is:
        |prof name
        -|stat
        --|weapon class
        ---|weapon name
        ----|value

    parameters:
        - data: The list obtained from the scrub method
        - prof: The name of the profile the stats are for as a string
    returns:
        - s_c_dict: A dictionary containing the information in the data list
                    in the stats_class format
    raises:
        ValueError: Raised when:
                        - the number of elements in the data list is not a
                          multiple of the known number of entries there are
                          for each weapon
                        - one of the stats entries in the data list is not
                          of a type that is known to be present.
    """
    stats = ["kills", "kpm", "time played", "shots fired", "shots hit",
             "accuracy", "headshots"]
    # this variable represents the total number of elements in the list that
    # belong to a single weapon
    ent = len(stats) + 2

    s_c_dict = {}
    s_c_dict[prof] = {}
    for i in stats:
        s_c_dict[prof][i] = {}

    if len(data) % ent != 0:
        raise ValueError("The number of entries in the scrubbed data was not a"
                         " multiple of {}. This may be the result of the"
                         " webpage changing its format or an unforseen entry"
                         " in a weapon stat field.".format(ent))

    # len(data)/ent gives the number of weapons present in the data
    for i in range(int(len(data)/ent)):
        for stat in stats:

            # if weapon class not in the stat part of dict make empty dict
            if data[i*ent + 1] not in s_c_dict[prof][stat].keys():
                s_c_dict[prof][stat][data[i*ent + 1]] = {}

            try:
                if stat in ["kpm", "accuracy"]:
                    s_c_dict[prof][stat][data[i*ent + 1]][data[i*ent]] = (
                        float(sub(",", "", data[i*ent + 2
                                                + stats.index(stat)])))
                elif (stat
                      in ["kills", "shots fired", "shots hit", "headshots"]):
                    s_c_dict[prof][stat][data[i*ent + 1]][data[i*ent]] = (
                        int(sub(",", "", data[i*ent + 2 + stats.index(stat)])))
                else:
                    s_c_dict[prof][stat][data[i*ent + 1]][data[i*ent]] = (
                        time_played.hours(data[i*ent + 2 + stats.index(stat)]))

            except ValueError:
                raise ValueError("One of the stats read in is not of the type"
                                 " expected.")

    return s_c_dict


def fillout(s_c_dict):
    """Adds 0 to weapon entries that exist in other profiles.

    The methods looks at all the weapon entries under a profile and upon
    finding one that exists in another profile an entry for that weapon is
    created and given the value 0. This was created as weapons that have not
    been used by a player will result in the weapon not appearing on the
    battlefield tracker website.

    parameters:
        - s_c_dict: the s_c_dict to be filled out
    returns:
    raises:
    """
    if len(s_c_dict) < 2:
        raise ValueError("There are not 2 or more profiles present in the"
                         " given s_c_dict")
    profs = list(s_c_dict.keys())
    mast_prof = profs[0]
    del profs[0]
    for prof in profs:
        for stat in s_c_dict[prof]:
            if stat not in s_c_dict[mast_prof].keys():
                s_c_dict[mast_prof][stat] = {}
            for w_class in s_c_dict[prof][stat].keys():
                if w_class not in s_c_dict[mast_prof][stat].keys():
                    s_c_dict[mast_prof][stat][w_class] = {}
                for weap in s_c_dict[prof][stat][w_class].keys():
                    if weap not in s_c_dict[mast_prof][stat][w_class].keys():
                        s_c_dict[mast_prof][stat][w_class][weap] = 0

    for prof in profs:
        for stat in s_c_dict[mast_prof].keys():
            if stat not in s_c_dict[prof].keys():
                s_c_dict[prof][stat] = {}
            for w_class in s_c_dict[mast_prof][stat].keys():
                if w_class not in s_c_dict[prof][stat].keys():
                    s_c_dict[prof][stat][w_class] = {}
                for weap in s_c_dict[mast_prof][stat][w_class].keys():
                    if weap not in s_c_dict[prof][stat][w_class].keys():
                        s_c_dict[prof][stat][w_class][weap] = 0


def add_hpk(stats_dict):
    """Add headshots per kill stat to given s_c dict.

    parameters:
        -stats_dict: The s_c dict to store the stat calculations to
    returns:

    raises:
        - ValueError: Various empty stats_dict keys that should have keys
                      present or stats that don't have the same weapon class
                      or weapons present
    """
    for prof in stats_dict.keys():
        if ("headshots" not in stats_dict[prof].keys()
                or "kills" not in stats_dict[prof].keys()):
            raise ValueError("The kills or headshots stats are not present")
        if len(stats_dict[prof]["headshots"].keys()) == 0:
            raise ValueError("There are no weapon classes present in the"
                             " headshots stat")
        if (stats_dict[prof]["headshots"].keys()
                != stats_dict[prof]["kills"].keys()):
            raise ValueError("headshots and kills do not have the"
                             " same weapon classes present in the"
                             " dictionary")
        stats_dict[prof]["hpk"] = {}

        for w_class in stats_dict[prof]["headshots"].keys():
            if len(stats_dict[prof]["headshots"][w_class].keys()) == 0:
                del stats_dict[prof]["hpk"]
                raise ValueError("There are no weapons in the {} class for"
                                 " headshots"
                                 .format(w_class))
            if (stats_dict[prof]["headshots"][w_class].keys()
                    != stats_dict[prof]["kills"][w_class].keys()):
                del stats_dict[prof]["hpk"]
                raise ValueError("heashots and kills do not have the same"
                                 " weapons present in the dictionary")
            stats_dict[prof]["hpk"][w_class] = {}

            for weap in stats_dict[prof]["headshots"][w_class].keys():
                try:
                    stats_dict[prof]["hpk"][w_class][weap] = (
                        stats_dict[prof]["headshots"][w_class][weap]
                        /stats_dict[prof]["kills"][w_class][weap]*100.0)
                except ZeroDivisionError:
                    stats_dict[prof]["hpk"][w_class][weap] = 0


def stat_limits(stats_dict, prof, stat, up_buff=None, low_buff=None):
    """Returns the highest and lowest values found in the s_c_dict provided.

    parameter:
        - stats_dict: The s_c_dict the min max values are wanted from
        - prof: The profile name the values are to be taken from as a string
        - stat: The stat the values are to be taken from as a string
        - up_buff: A value indicating the amount of buffer desired as a
                   percentage of on the max value
        - low_buff: A value indicating the amount of buffer desired as a
                    percentage of the minimum value
    returns:
        - s_min: The smallest value among those for a particular stat and
                 weapon class provided
        - s_max: The largest value ""
    raises:
    """
    s_min = 0
    s_max = 0
    for w_class in stats_dict[prof][stat].keys():
        for weap in stats_dict[prof][stat][w_class].keys():
            if stats_dict[prof][stat][w_class][weap] > s_max:
                s_max = stats_dict[prof][stat][w_class][weap]
            if stats_dict[prof][stat][w_class][weap] < s_min:
                s_min = stats_dict[prof][stat][w_class][weap]

    if up_buff is not None:
        s_max = s_max + abs(s_max*up_buff)

    if low_buff is not None:
        s_min = s_min - abs(s_min*low_buff)

    return s_min, s_max
