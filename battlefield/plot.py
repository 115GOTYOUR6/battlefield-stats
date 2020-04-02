# File: plot.py
# Author: Jay Oliver
# Date Created: 29/03/2020
# Last Modified: 2/04/2020
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

import matplotlib.pyplot as plt
from re import sub
from os import mkdir

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
        "accuracy": "(shots hit/shots fired)"
    }
    return switcher.get(stat, "")


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




def s_c_plot(stats_dict, dname, stats2plot=None):
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
    # search for the heighest values before making the plots as there is to
    # many (potentially) to hold them in buffer, modify and then save   
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
                                     " {}".format(prof))
        try:
            mkdir("{}/{}".format(dname, prof))
        except FileExistsError:
            pass
        for stat in stats2plot:
            try:
                mkdir("{}/{}/{}".format(dname, prof, stat))
            except FileExistsError:
                pass
            for w_class in stats_dict[prof][stat].keys():
                fig = plt.figure(figsize = (23, 14), facecolor = 'w')
                weap_dict = stats_dict[prof][stat][w_class]
                plt.bar([i for i in range(len(weap_dict.keys()))],
                        [weap_dict[j] for j in weap_dict.keys()],
                        tick_label = [k for k in weap_dict.keys()])
                plt.suptitle("{} {} for {}S".format(prof, stat, w_class),
                            fontsize = 16)
                plt.ylabel("{} {}".format(stat, stat_units(stat)))
                plt.savefig("{}/{}/{}/{} {} for {}S"
                           ".png".format(dname, prof, stat, prof, stat,
                                         w_class),
                           bbox_inches = "tight")
                plt.close(fig=None)
