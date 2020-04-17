# File: overview.py
# Author: Jay Oliver
# Date Created: 14/04/2020
# Date Last Modified: 17/04/2020
# Purpose: Contains all methids relating to the creation and modifycation of
#           overstat dictionaries for the battlefield_stats program
# Comments:

from re import sub


def over_form(data, prof):
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
                             -|soldier class
                             --|stat
                             ---|value
    raises:
        ValueError: When an entry obtained from the list is not of the type
                    expected given the stat it is supposed to be for
    """
    c_stats = ["rank", "score", "score/min", "kills", "kpm", "k/d"]

    # these marks show where the entry for the top class occurs
    mark = min([data.index(i) for i
                in ["Support", "Assault", "Recon", "Medic"]])
    if len(data[:mark]) % 2 != 0:
        raise ValueError("The career stat entries do not make a multiple of"
                         " 2, likely because of a bad splice or one of the"
                         " career stats not having a header.")
    over_dict = {}
    over_dict[prof] = {}
    # store the carrer stats first
    for i in range(int(len(data[:mark])/2)):
        if data[i*2] not in over_dict[prof].keys():
            over_dict[prof][data[i*2]] = {}
        if data[i*2] in ["Win %", "K/D", "Kills/min", "Score/min"]:
            over_dict[prof][data[i*2]]["career"] = float(data[i*2 + 1][:-1])
        elif data[i*2] in ["Assists", "Damage", "Deaths", "Heals", "Kills",
                           "Resupplies", "Revives", "Wins"]:
            over_dict[prof][data[i*2]]["career"] = int(sub(",", "",
                                                           data[i*2 + 1]))
        else:
            over_dict[prof][data[i*2]]["career"] = int(data[i*2 + 1])
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
        over_dict[prof][stat] = {}
        for i in range(int(len(c_list)/c_size)):
            try:
                if stat in ["score/min", "kpm", "k/d"]:
                    over_dict[prof][stat][c_list[i*c_size]] = (
                        float(c_list[i*c_size + 1 + c_stats.index(stat)]))
                elif stat in ["score", "kills"]:
                    over_dict[prof][stat][c_list[i*c_size]] = (
                        int(sub(",", "", c_list[i*c_size
                                                + 1 + c_stats.index(stat)])))
                else:
                    over_dict[prof][stat][c_list[i*c_size]] = (
                        int(c_list[i*c_size + 1 + c_stats.index(stat)]))
            except ValueError:
                raise ValueError("One of the stats was not of the type"
                                 " expected.")
    return over_dict
