# File: plot.py
# Author: Jay Oliver
# Date Created: 29/03/2020
# Last Modified: 6/04/2020
# Purpose: Creates bar graphs displaying stats from the battlefield tracker
#          website. Specifically the ouput of the scrub module in the
#          battlefield package
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
#

import matplotlib.pyplot as plt
from re import sub
from os import mkdir
from math import ceil

from battlefield import time_played

def stat_units(stat):
    """Returns the units for the provided stat.

    parameters
        - stat: The stat the units are wanted for.
    return
        - switcher.get: Gets the stat value from the dictionary switcher. Upon
                        failing to retreive anything it returns an empty
                        string.
    raises:
    """
    switcher = {
        "kpm": "(kills/min)",
        "time played": "(hours)",
        "accuracy": "(shots hit/shots fired)",
        "hpk": "(headshot percentage)"
    }
    return switcher.get(stat, "")

def zero_to_ten(val):
    """Returns the given value if in the range of 0 to 10 otherwise these
    boundary values are returned.

    parameters:
        - val: The number to check is in range 0 - 10 and return if it is
    returns:
        - ret:
    raises
    """
    if val <= 0:
        ret = 0
    elif val >= 10:
        ret = 10
    else:
        ret = val
    return ret



def s_c_limits(stats_dict, prof, stat, up_buff = None, low_buff = None):
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

    if up_buff != None:
        s_max = s_max + abs(s_max*up_buff)

    if low_buff != None:
        s_min = s_min - abs(s_min*low_buff)

    return s_min, s_max


# s_c meaning stat class
def s_c_form(data, prof):
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
                        float(data[i*ent + 2 + stats.index(stat)])
                    )
                elif (stat
                      in ["kills", "shots fired", "shots hit", "headshots"]):
                   s_c_dict[prof][stat][data[i*ent + 1]][data[i*ent]] = (
                       int(sub(",", "", data[i*ent + 2 + stats.index(stat)]))
                   )
                else:
                    s_c_dict[prof][stat][data[i*ent + 1]][data[i*ent]] = (
                        time_played.hours(data[i*ent + 2 + stats.index(stat)])
                    )

            except ValueError:
                raise ValueError("One of the stats read in is not of the type"
                                 " expected.")

    return s_c_dict

def s_c_add_hpk(stats_dict):
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
                             " headshots stat"
                            )
        if (stats_dict[prof]["headshots"].keys()
            != stats_dict[prof]["kills"].keys()):
            raise ValueError("headshots and kills do not have the"
                            " same weapon classes present in the"
                            " dictionary"
                            )
        stats_dict[prof]["hpk"] = {}

        for w_class in stats_dict[prof]["headshots"].keys():
            if len(stats_dict[prof]["headshots"][w_class].keys()) == 0:
                del(stats_dict[prof]["hpk"])
                raise ValueError("There are no weapons in the {} class for"
                                 " headshots"
                                 .format(w_class)
                                )
            if (stats_dict[prof]["headshots"][w_class].keys()
                != stats_dict[prof]["kills"][w_class].keys()):
                    del(stats_dict[prof]["hpk"])
                    raise ValueError("heashots and kills do not have the same"
                                    " weapons present in the dictionary"
                                    )
            stats_dict[prof]["hpk"][w_class] = {}

            for weap in stats_dict[prof]["headshots"][w_class].keys():
                try:
                    stats_dict[prof]["hpk"][w_class][weap] = (
                        stats_dict[prof]["headshots"][w_class][weap]
                        /stats_dict[prof]["kills"][w_class][weap]*100.0
                    )
                except ZeroDivisionError:
                    stats_dict[prof]["hpk"][w_class][weap] = 0


def some_format(stats_list):
    """Incomplete function to convert the stats list to a dict.

    Intended format is:
        |profile name
        -|weapon class
        --|weapon name
        ---|stat (such as kills, kpm etc.)
        ----|value


    """
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




def s_c_plot(stats_dict, dname, stats2plot = None, up_buff = None):
    """Creates bar graphs from the data in the given dictionary.

    The data is that obtained from the s_c_format method in this module.

    parameters:
        - stats_dict: A dictionary containing the stats for weapons.
        - dname:
        - stats2plot: A list of strings indicating the stats that are to be
                      plotted, if this parameter is not given all the
                      available stats will be graphed.
    returns:
    raises:
        - ValueError: If the type of the optional parameter is not a list of
                      strings or one of the stats given to be plotted is not
                      in the data set this is raised.
    """
    if stats2plot != None:
        if not isinstance(stats2plot, list):
            raise ValueError("The optional parameter stats2plot is not a"
                             "list."
                            )
        for i in stats2plot:
            if not isinstance(i, str):
                raise ValueError("One or more of the elements of the"
                                 " optional list stats2plot is not a string."
                                )
    try:
        mkdir(dname)
    except FileExistsError:
        pass


    for prof in stats_dict.keys():
        if stats2plot == None:
            stats2plot = stats_dict[prof].keys()
        else:
            for i in stats2plot:
                if i not in stats_dict[prof].keys():
                    raise ValueError("One of the specified stats to plot is"
                                     " not present in the weapon stats for"
                                     " {}".format(prof)
                                    )
        try:
            mkdir("{}/{}".format(dname, prof))
        except FileExistsError:
            pass
        for stat in stats2plot:
            try:
                mkdir("{}/{}/{}".format(dname, prof, stat))
            except FileExistsError:
                pass
            if up_buff != None:
                y_min, y_max = s_c_limits(stats_dict, prof, stat,
                                          up_buff = up_buff)
            else:
                y_min, y_max = s_c_limits(stats_dict, prof, stat)

            for w_class in stats_dict[prof][stat].keys():
                # define some variables to shorten lines
                w_dict = stats_dict[prof][stat][w_class]
                w_keys = [i for i in w_dict.keys()]
                for pnum in range(ceil(len(w_keys)/10)):
                    # define a couple more variables
                    keys_to_plot = w_keys[pnum*10:
                                          pnum*10 + zero_to_ten(len(w_keys)
                                                                - pnum*10)]
                    x = [i for i in range(zero_to_ten(len(keys_to_plot)))]
                    y = [w_dict[j] for j in keys_to_plot]

                    fig = plt.figure(figsize = (23, 14), facecolor = 'w')
                    plt.bar(x, y,
                            tick_label = [k for k in keys_to_plot]
                           )
                    plt.ylabel("{} {}".format(stat, stat_units(stat)))
                    plt.ylim(y_min, y_max)
                    for bar in x:
                        plt.text(bar,
                                 y[bar] + plt.ylim()[1]*0.01,
                                 y[bar],
                                 horizontalalignment="center"
                                )
                    if len(w_keys) > 10:
                        plt.suptitle("{} {} for {}S {}".format(prof, stat,
                                                               w_class,
                                                               pnum+1),
                                    fontsize = 16
                                    )
                        plt.savefig("{}/{}/{}/{} {} for {}S {}"
                                    ".png".format(dname, prof, stat, prof,
                                                  stat, w_class, pnum+1),
                                    bbox_inches = "tight"
                                   )

                    else:
                        plt.suptitle("{} {} for {}S".format(prof, stat,
                                                            w_class),
                                    fontsize = 16
                                    )
                        plt.savefig("{}/{}/{}/{} {} for {}S"
                                    ".png".format(dname, prof, stat, prof, stat,
                                                  w_class),
                                    bbox_inches = "tight"
                                   )
                    plt.close(fig=None)
