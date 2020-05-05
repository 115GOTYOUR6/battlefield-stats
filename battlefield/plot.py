# File: plot.py
# Author: Jay Oliver
# Date Created: 29/03/2020
# Last Modified: 05/05/2020
# Purpose: Creates bar graphs displaying stats from the battlefield tracker
#          website.
#
# Comments:
#

from re import sub
from os import mkdir
from math import ceil
import matplotlib.pyplot as plt

from battlefield import overview
from battlefield import weapons
from battlefield import directories as dirs


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
        "hpk": "(headshot percentage)"}
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
    if len(profs) > 4 or len(profs) < 2:
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


def weap_plot(stats_dict, dname, stats2plot=None, up_buff=None):
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
    if stats2plot is not None:
        if not isinstance(stats2plot, list):
            raise ValueError("The optional parameter stats2plot is not a"
                             "list.")
        for i in stats2plot:
            if not isinstance(i, str):
                raise ValueError("One or more of the elements of the"
                                 " optional list stats2plot is not a string.")

    for prof in stats_dict.keys():
        if stats2plot is None:
            stats2plot = stats_dict[prof].keys()
        else:
            for i in stats2plot:
                if i not in stats_dict[prof].keys():
                    raise ValueError("One of the specified stats to plot is"
                                     " not present in the weapon stats for"
                                     " {}".format(prof))

        path = "{}/{}/weapons".format(dname, prof)
        for stat in stats2plot:
            dirs.create_pwd("{}/{}".format(path, stat))
            if up_buff is not None:
                y_min, y_max = weapons.stat_limits(stats_dict, prof, stat,
                                                   up_buff=up_buff)
            else:
                y_min, y_max = weapons.stat_limits(stats_dict, prof, stat)

            for w_class in stats_dict[prof][stat].keys():
                w_dict = stats_dict[prof][stat][w_class]
                # this is required as keys cannot be sliced
                w_keys = [i for i in w_dict.keys()]
                for pnum in range(ceil(len(w_keys)/10)):
                    # define a couple more variables
                    keys_to_plot = w_keys[pnum*10:
                                          pnum*10 + zero_to_ten(len(w_keys)
                                                                - pnum*10)]
                    x = [i for i in range(zero_to_ten(len(keys_to_plot)))]
                    y = [w_dict[j] for j in keys_to_plot]

                    plt.figure(figsize=(23, 14), facecolor='w')
                    plt.bar(x, y,
                            tick_label=keys_to_plot)
                    plt.ylabel("{} {}".format(stat, stat_units(stat)))
                    plt.ylim(y_min, y_max)
                    for rect in x:
                        if (isinstance(y[rect], float)
                                and round(y[rect], 2) != 0):
                            plt.text(rect,
                                     y[rect] + plt.ylim()[1]*0.01,
                                     "{:.2f}".format(y[rect]),
                                     horizontalalignment="center"
                                     )
                        elif (isinstance(y[rect], float)
                              and round(y[rect], 2) == 0):
                            plt.text(rect,
                                     y[rect] + plt.ylim()[1]*0.01,
                                     "0",
                                     horizontalalignment="center")
                        else:
                            plt.text(rect,
                                     y[rect] + plt.ylim()[1]*0.01,
                                     y[rect],
                                     horizontalalignment="center")

                    if len(w_keys) > 10:
                        plt.suptitle("{} {} for {}S {}".format(prof, stat,
                                                               w_class,
                                                               pnum+1),
                                     fontsize=16)
                        plt.savefig("{}/{}/{} {} for {}S {}"
                                    ".png".format(path, stat, prof,
                                                  stat, w_class, pnum+1),
                                    bbox_inches="tight")

                    else:
                        plt.suptitle("{} {} for {}S".format(prof, stat,
                                                            w_class),
                                     fontsize=16)
                        plt.savefig("{}/{}/{} {} for {}S"
                                    ".png".format(path, stat, prof,
                                                  stat, w_class),
                                    bbox_inches="tight")
                    plt.close(fig=None)


def weap_comp_plot(stats_dict, dname, stats2plot=None, up_buff=None):
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
    if stats2plot is not None:
        if not isinstance(stats2plot, list):
            raise ValueError("The optional parameter stats2plot is not a"
                             "list.")
        for i in stats2plot:
            if not isinstance(i, str):
                raise ValueError("One or more of the elements of the"
                                 " optional list stats2plot is not a string.")
    if len(stats_dict.keys()) > 4 or len(stats_dict.keys()) < 2:
        raise ValueError("The given s_c_dict does not have the supported"
                         " number of profiles present (2-4).")
    # ensure that the dictionary has the same entries for each stat
    weapons.fillout(stats_dict)
    profs = sorted(list(stats_dict.keys()))
    m_prof = profs[0]
    comp_pname = " vs ".join(profs)
    if stats2plot is None:
        stats2plot = stats_dict[m_prof].keys()
    else:
        for i in stats2plot:
            if i not in stats_dict[m_prof].keys():
                raise ValueError("One of the specified stats to plot is"
                                 " not present in the weapon stats for"
                                 " {}".format(m_prof))
    if dname[-1] == "/":
        dname = dname[:-1:]
    path = "{}/{}/weapons".format(dname, comp_pname)
    for stat in stats2plot:
        dirs.create_pwd("{}/{}".format(path, stat))
        # these maybe configurable in future version
        width = 0.8
        plot_params = comp_plot_params(profs, width)
        y_min = 0
        y_max = 0
        # find the min max values for the stat among all the profiles
        for prof in profs:
            if up_buff is not None:
                min_tem, max_tem = weapons.stat_limits(stats_dict, prof, stat,
                                                       up_buff=up_buff)
                if y_min > min_tem:
                    y_min = min_tem
                if y_max < max_tem:
                    y_max = max_tem
            else:
                min_tem, max_tem = weapons.stat_limits(stats_dict, prof, stat)
                if y_min > min_tem:
                    y_min = min_tem
                if y_max < max_tem:
                    y_max = max_tem

        for w_class in stats_dict[m_prof][stat].keys():
            # cannot slice dict keys
            w_keys = [i for i in stats_dict[m_prof][stat][w_class]]
            for pnum in range(ceil(len(w_keys)/10)):
                # define a couple more variables
                weaps_to_plot = w_keys[pnum*10:
                                       pnum*10 + zero_to_ten(len(w_keys)
                                                             - pnum*10)]
                plt.figure(figsize=(23, 14), facecolor='w')
                for prof in profs:
                    x = [i + plot_params[prof]['x_pos']
                         for i in range(zero_to_ten(len(weaps_to_plot)))]
                    y = [stats_dict[prof][stat][w_class][j] for j
                         in weaps_to_plot]
                    plt.bar(x, y,
                            color=plot_params[prof]['col'],
                            label=prof,
                            width=width/len(profs))
                    for ind in range(len(x)):
                        if isinstance(y[ind], float) and round(y[ind], 2) != 0:
                            plt.text(x[ind],
                                     y[ind] + plt.ylim()[1]*0.01,
                                     "{:.2f}".format(y[ind]),
                                     horizontalalignment="center")
                        elif (isinstance(y[ind], float)
                              and round(y[ind], 2) == 0):
                            plt.text(x[ind],
                                     y[ind] + plt.ylim()[1]*0.01,
                                     "0",
                                     horizontalalignment="center")
                        else:
                            plt.text(x[ind],
                                     y[ind] + plt.ylim()[1]*0.01,
                                     y[ind],
                                     horizontalalignment="center")

                plt.xticks(ticks=range(zero_to_ten(len(weaps_to_plot))),
                           labels=weaps_to_plot)
                plt.ylabel("{} {}".format(stat, stat_units(stat)))
                plt.ylim(y_min, y_max)
                plt.legend(loc="upper right")

                if len(w_keys) > 10:
                    plt.suptitle("{} {} for {}S {}".format(comp_pname, stat,
                                                           w_class,
                                                           pnum+1),
                                 fontsize=16)
                    plt.savefig("{}/{}/{} {} for {}S {}"
                                ".png".format(path, stat, stat, comp_pname,
                                              w_class, pnum+1),
                                bbox_inches="tight")

                else:
                    plt.suptitle("{} {} for {}S".format(comp_pname, stat,
                                                        w_class),
                                 fontsize=16)
                    plt.savefig("{}/{}/{} {} for {}S"
                                ".png".format(path, stat, stat, comp_pname,
                                              w_class),
                                bbox_inches="tight")
                plt.close(fig=None)


def over_comp_plot(over_dict, dname, stats2plot=None, up_buff=None):
    """Plots the data obtained by scrubbing the overview page.

    parameters:
        - over_dict: The dictionary containing the data to be plotted
        - dname: The name of the directory the created figures are to
                 be saved to
        - stats2plot: The stats that figures are to be made for
        - up_buff: A buffer as a percentage of the highest value for each stat,
                   this is used to set the y axis max value so that the top
                   of the figure is above the highest bar, thus leaving space
                   for the numbers above the bars
    raises:
        ValueError: When a parameter or a value contained within one is not
                    of the desired type
    """
    if stats2plot is not None:
        if not isinstance(stats2plot, list):
            raise ValueError("The optional parameter stats2plot is not a"
                             "list.")
        for i in stats2plot:
            if not isinstance(i, str):
                raise ValueError("One or more of the elements of the"
                                 " optional list stats2plot is not a string.")
    if len(over_dict.keys()) > 4 or len(over_dict.keys()) < 2:
        raise ValueError("The given over_dict does not have the supported"
                         " number of profiles present (2-4).")
    profs = sorted(list(over_dict.keys()))
    m_prof = profs[0]
    if dname[-1] == "/":
        dname = dname[:-1:]
    comp_pname = " vs ".join(profs)
    path = dname + "/" + comp_pname + "/" + "overview"
    files = dirs.create_pwd(path)
    if stats2plot is None:
        stats2plot = over_dict[m_prof].keys()
    else:
        for i in stats2plot:
            if i not in over_dict[m_prof].keys():
                dirs.remove_pwd(files)
                raise ValueError("One of the specified stats to plot is"
                                 " not present in the class stats for"
                                 " {}".format(m_prof))
    # these maybe configurable in future version
    width = 0.8
    plot_params = comp_plot_params(profs, width)

    for stat in stats2plot:
        plt.figure(figsize=(23, 14), facecolor='w')
        y_min = 0
        y_max = 0
        s_class_keys = over_dict[m_prof][stat].keys()
        for prof in profs:
            # find the limits
            if up_buff is not None:
                min_tem, max_tem = overview.stat_limits(over_dict, prof,
                                                        stat,
                                                        up_buff=up_buff)
                if y_min > min_tem:
                    y_min = min_tem
                if y_max < max_tem:
                    y_max = max_tem
            else:
                min_tem, max_tem = overview.stat_limits(over_dict, prof,
                                                        stat)
                if y_min > min_tem:
                    y_min = min_tem
                if y_max < max_tem:
                    y_max = max_tem
            x = [i + plot_params[prof]['x_pos']
                 for i in range((len(over_dict[prof][stat].keys())))]
            y = [over_dict[prof][stat][j] for j
                 in s_class_keys]
            plt.bar(x, y,
                    color=plot_params[prof]['col'],
                    label=prof,
                    width=width/len(profs))
            for ind in range(len(x)):
                # add some numbers to plot
                if isinstance(y[ind], float) and round(y[ind], 2) != 0:
                    plt.text(x[ind],
                             y[ind] + plt.ylim()[1]*0.01,
                             "{:.2f}".format(y[ind]),
                             horizontalalignment="center")
                elif (isinstance(y[ind], float)
                      and round(y[ind], 2) == 0):
                    plt.text(x[ind],
                             y[ind] + plt.ylim()[1]*0.01,
                             "0",
                             horizontalalignment="center")
                else:
                    plt.text(x[ind],
                             y[ind] + plt.ylim()[1]*0.01,
                             y[ind],
                             horizontalalignment="center")
        plt.xticks(ticks=range((len(x))),
                   labels=s_class_keys)
        plt.ylabel("{} {}".format(stat, stat_units(stat)))
        plt.ylim(y_min, y_max)
        plt.legend(loc="upper right")
        plt.suptitle("{} for {}".format(comp_pname, stat),
                     fontsize=16)
        plt.savefig("{}/{} {}.png".format(path, comp_pname,
                                          sub("/", "-", stat)),
                    bbox_inches="tight")
