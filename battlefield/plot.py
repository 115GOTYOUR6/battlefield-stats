# File: plot.py
# Author: Jay Oliver
# Date Created: 29/03/2020
# Last Modified: 9/04/2020
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

def s_c_fillout(s_c_dict):
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
                        " given s_c_dict"
                        )
    profs = list(s_c_dict.keys())
    mast_prof = profs[0]
    del(profs[0])
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

def comp_plot_params(profs, width):
    """Color and position on x axis is assigned for each profile.

    The method takes a list of profiles and the width of the bars that will
    appear in the s_c_comp_plot function and assigns plot parameters for each
    profile.

    parameters:
        - profs: a list of profile names
        - width: the width of the bars on the plot
    returns:
        - plot_params: the dictionary containing the parameters for each of
                       the profiles
    raises:
        - ValueError: When the input parameters are not of the expected type:
                        - profs = list
                        - width = float
                      or then the number of profiles given is not in the range
                      2-4

    """
    if not isinstance(width, float):
        raise ValueError("The width given is not a float")
    if not isinstance(profs, list):
        raise ValueError("The given parameter is not a list.")
    elif len(profs) > 4 or len(profs) < 2:
        raise ValueError("The number of profiles provided is not supported")

    cols = ['b', 'm', 'c', 'darkorange']
    if len(profs) == 2:
        x_pos = [-width/4, width/4]
    elif len(profs) == 3:
        x_pos = [-width/3, 0, width/3]
    else:
        x_pos = [-3*width/8, -width/8, width/8, 3*width/8]
    plot_params = {}

    for i in range(len(profs)):
        plot_params[profs[i]] = {}
        plot_params[profs[i]]["col"] = cols[i]
        plot_params[profs[i]]["x_pos"] = x_pos[i]

    return plot_params

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
                        if isinstance(y[bar], float):
                            plt.text(bar,
                                    y[bar] + plt.ylim()[1]*0.01,
                                     "{:.2f}".format(y[bar]),
                                    horizontalalignment="center"
                                    )
                        else:
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

def s_c_comp_plot(stats_dict, dname, stats2plot = None, up_buff = None):
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
    if len(stats_dict.keys()) > 4 or len(stats_dict.keys()) < 2:
        raise ValueError("The given s_c_dict does not have the supported"
                         " number of profiles present (2-4)."
                        )
    # ensure that the dictionary has the same entries for each stat
    s_c_fillout(stats_dict)
    try:
        mkdir(dname)
    except FileExistsError:
        pass
    profs = list(stats_dict.keys())
    m_prof = profs[0]
    comp_pname = " vs ".join(profs)
    if stats2plot == None:
        stats2plot = stats_dict[m_prof].keys()
    else:
        for i in stats2plot:
            if i not in stats_dict[m_prof].keys():
                raise ValueError("One of the specified stats to plot is"
                                " not present in the weapon stats for"
                                " {}".format(m_prof)
                                )
    try:
        mkdir("{}/{}".format(dname, comp_pname))
    except FileExistsError:
        pass
    for stat in stats2plot:
        try:
            mkdir("{}/{}/{}".format(dname, comp_pname, stat))
        except FileExistsError:
            pass
        width = 0.8
        plot_params = comp_plot_params(profs, width)
        y_min = 0
        y_max = 0
        # find the min max values for the stat among all the profiles
        for prof in profs:
            if up_buff != None:
                min_tem, max_tem = s_c_limits(stats_dict, m_prof, stat,
                                        up_buff = up_buff)
                if y_min > min_tem:
                    y_min = min_tem
                if y_max < max_tem:
                    y_max = max_tem
            else:
                min_tem, max_tem = s_c_limits(stats_dict, m_prof, stat)
                if y_min > min_tem:
                    y_min = min_tem
                if y_max < max_tem:
                    y_max = max_tem

        for w_class in stats_dict[m_prof][stat].keys():
            # define some variables to shorten lines
            w_keys = [i for i in stats_dict[m_prof][stat][w_class]]
            for pnum in range(ceil(len(w_keys)/10)):
                # define a couple more variables
                weaps_to_plot = w_keys[pnum*10:
                                      pnum*10 + zero_to_ten(len(w_keys)
                                                            - pnum*10)]
                fig = plt.figure(figsize = (23, 14), facecolor = 'w')
                for prof in profs:
                    x = [i + plot_params[prof]['x_pos']
                         for i in range(zero_to_ten(len(weaps_to_plot)))]
                    y = [stats_dict[prof][stat][w_class][j] for j in weaps_to_plot]
                    plt.bar(x, y,
                            color = plot_params[prof]['col'],
                            label = prof,
                            width = width/len(profs)
                           )
                    for ind in range(len(x)):
                        if isinstance(y[ind], float):
                            plt.text(x[ind],
                                    y[ind] + plt.ylim()[1]*0.01,
                                     "{:.2f}".format(y[ind]),
                                    horizontalalignment="center"
                                    )
                        else:
                            plt.text(x[ind],
                                    y[ind] + plt.ylim()[1]*0.01,
                                    y[ind],
                                    horizontalalignment="center"
                                    )

                plt.xticks(ticks = [i for i
                                    in range(zero_to_ten(len(weaps_to_plot)))],
                           labels = [k for k in weaps_to_plot]
                          )
                plt.ylabel("{} {}".format(stat, stat_units(stat)))
                plt.ylim(y_min, y_max)
                plt.legend(loc = "upper right")

                if len(w_keys) > 10:
                    plt.suptitle("{} {} for {}S {}".format(comp_pname, stat,
                                                          w_class,
                                                          pnum+1
                                                          ),
                                fontsize = 16
                                )
                    plt.savefig("{}/{}/{}/{} {} for {}S {}"
                                ".png".format(dname,
                                              comp_pname, stat, stat,
                                              comp_pname, w_class, pnum+1
                                             ),
                                bbox_inches = "tight"
                               )

                else:
                    plt.suptitle("{} {} for {}S".format(comp_pname, stat,
                                                        w_class
                                                       ),
                                fontsize = 16
                                )
                    plt.savefig("{}/{}/{}/{} {} for {}S"
                                ".png".format(dname,comp_pname, stat,
                                              stat, comp_pname, w_class
                                             ),
                                bbox_inches = "tight"
                               )
                plt.close(fig=None)
