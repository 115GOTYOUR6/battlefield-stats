# File: overview.py
# Author: Jay Oliver
# Date Created: 14/04/2020
# Date Last Modified: 05/05/2020
# Purpose: Contains all methids relating to the creation and modifycation of
#           overstat dictionaries for the battlefield_stats program
# Comments:

from re import sub


def create(data, prof):
    """Put the information obtained from the scub module into a dictionary.

    The parsed stats from the website given as data here from the scrub module
    is formatted like so:
        - career stats, with headers
        ...
        ...
        - Top Class stats
        - Class stats

    parameters:
        - data: a list containing the data parsed from battlefield tracker
                website. It has a form illustrated above
        - prof: a string representing the profile name the stats are for
    returns:
        - overstat_dict: A dictionary containing the stats from the list
                         organised like so:
                             |profile name
                             -|stat
                             --|soldier class
                             ---|value
    raises:
        ValueError: When an entry obtained from the list is not of the type
                    expected given the stat it is supposed to be for
    """
    c_stats = ["rank", "score", "score/min", "kills", "kills/min", "k/d"]

    # these marks show where the entry for the top class occurs
    mark = min([data.index(i) for i
                in ["Support", "Assault", "Recon", "Medic"]])
    if len(data[:mark]) % 2 != 0:
        raise ValueError("The career stat entries do not make a multiple of"
                         " 2, likely because of a bad splice or one of the"
                         " career stats not having a header.")
    over_dict = {}
    over_dict[prof] = {}
    # store the carrer stats first, career stats all start with a capital
    # hence casefold
    for i in range(int(len(data[:mark])/2)):
        if data[i*2].casefold() not in over_dict[prof].keys():
            over_dict[prof][data[i*2].casefold()] = {}
        if data[i*2].casefold() in ["win %", "k/d", "kills/min", "score/min"]:
            over_dict[prof][data[i*2].casefold()]["Career"] = float(
                data[i*2 + 1][:-1])
        elif data[i*2].casefold() in ["assists", "damage", "deaths", "heals",
                                      "kills", "resupplies", "revives",
                                      "wins"]:
            over_dict[prof][data[i*2].casefold()]["Career"] = int(
                sub(",", "", data[i*2 + 1]))
        else:
            over_dict[prof][data[i*2].casefold()]["Career"] = int(
                data[i*2 + 1])
    # mark + 1 will exclude the name of the top class so that the next class
    # reference can be found which should be the start of the class stats
    # entries
    mark2 = min([data[mark + 1:].index(i) + mark + 1 for i
                 in ["Support", "Assault", "Recon", "Medic"]])
    c_list = data[mark2:]
    c_size = len(c_stats) + 1
    if len(c_list) % c_size != 0:
        raise ValueError("The list of class stats is not the size that it was"
                         " expected to be. This maybe because a stat was"
                         " added")
    for stat in c_stats:
        if stat not in over_dict[prof].keys():
            over_dict[prof][stat] = {}
        for i in range(int(len(c_list)/c_size)):
            try:
                if stat in ["score/min", "kills/min", "k/d"]:
                    over_dict[prof][stat][c_list[i*c_size]] = (
                        float(sub(",", "", c_list[i*c_size + 1
                                                  + c_stats.index(stat)])))
                elif stat in ["score", "kills"]:
                    over_dict[prof][stat][c_list[i*c_size]] = (
                        int(sub(",", "", c_list[i*c_size
                                                + 1 + c_stats.index(stat)])))
                else:
                    over_dict[prof][stat][c_list[i*c_size]] = (
                        int(sub(",", "", c_list[i*c_size + 1
                                                + c_stats.index(stat)])))
            except ValueError:
                raise ValueError("One of the stats was not of the type"
                                 " expected.")
    return over_dict


def copy(over_dict, classes=None):
    """Creates a copy of a overview dictionary.

    parameters:
        - over_dict: The overview dictionary that is to be copied
        - classes: The soldier classes that are to be included. If this is
                   left empty an exact copy is returned
    returns:
        - copy_dict: The copy of over_dict only containing the specified
                     soldier classes
    """
    if classes is None:
        classes = []
    copy_dict = {}
    for prof in over_dict.keys():
        for stat in over_dict[prof].keys():
            for s_class in over_dict[prof][stat].keys():
                if s_class in classes or len(classes) == 0:
                    if prof not in copy_dict.keys():
                        copy_dict[prof] = {}
                    if stat not in copy_dict[prof].keys():
                        copy_dict[prof][stat] = {}
                    copy_dict[prof][stat][s_class] = (over_dict[prof][stat]
                                                      [s_class])
                else:
                    pass
    return copy_dict


def stat_limits(over_dict, prof, stat, up_buff=None, low_buff=None):
    """Find the highest and lowest value for the given stat and profile.

    parameters:
        - over_dict: A dictionary containing information scrubbed from the
                     overview page of the battlefield tracker website
        - prof: a string representing the profile name the stats are for
        - stat: a string, the stat the limits are to be found for
    returns:
        - s_min: the lowest stat value
        - s_max: the largest stat value
    """
    s_min = 0
    s_max = 0
    for s_class in over_dict[prof][stat].keys():
        if over_dict[prof][stat][s_class] > s_max:
            s_max = over_dict[prof][stat][s_class]
        if over_dict[prof][stat][s_class] < s_min:
            s_min = over_dict[prof][stat][s_class]

    if up_buff is not None:
        s_max = s_max + abs(s_max*up_buff)
    if low_buff is not None:
        s_min = s_min - abs(s_min*low_buff)

    return s_min, s_max
