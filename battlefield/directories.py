# Author: Jay Oliver
# Date Created: 03/05/2020
# Date Last Modified: 05/05/2020
# Purpose: Contains functions that pertain to directory manipulation
# Comments:

from os import mkdir
from os import rmdir


def create_dir(direct):
    """Create the given directory in the present working directory.

    The present working directory is taken as the location of invokation.
    parameters:
        - direct: A string, the file path to be created
    returns:
        - files: A dictionary containg information about the file path created
                 the structure is as follows:
                    |path  (direct parameter eg. "some/thing")
                    |0     (The first file in the path. A 0 is stored if the
                    |1        creation of the file failed, a 1 on success.)
                    ...
    raises:
        - TypeError: When the given parameter is not of the expected type
    """
    if not isinstance(direct, str):
        raise TypeError("The given parameter is not a sting")
    if direct[-1] == '/':
        direct = direct[:-1:]

    files = {}
    files["path"] = direct
    path = ""
    for ind, val in enumerate(direct.split('/')):
        try:
            if val == '':
                val = '/'
            path = path + val
            mkdir(path)
            files[ind] = 1
        except FileExistsError:
            files[ind] = 0
        path = path + '/'
    return files


def remove_dir(files):
    """Remove the files marked as created by create_pwd

    parameters:
        - files: The dictionary returned by create_pwd containing the files
                 created. The structure is as follows:
                    |path  (direct parameter eg. "some/thing")
                    |0     (The first file in the path. A 0 is stored if the
                    |1        creation of the file failed, a 1 on success.)
                    ...
    raises:
        - TypeError: When the given parameter does not meet the expected type
        - ValueError: When the 'path' key of the dictionary, files, is not
                      present.
    """
    if not isinstance(files, dict):
        raise TypeError("The given parameter is not a dictionary")
    if "path" not in files.keys():
        raise ValueError("The directory created is not recorded in the"
                         " given dictionary")

    for i in reversed(range(len(files.keys()) - 1)):
        if not isinstance(files[i], int):
            raise TypeError("The {i} entry in the given parameter is not"
                            " an integer".format(i=i))
        if files[i] == 1:
            try:
                rm_file = "/".join(files['path'].split("/")[:i + 1:])
                if rm_file == "/":
                    pass
                elif rm_file == "/home":
                    pass
                else:
                    rmdir(rm_file)
            except OSError:
                raise OSError("A directory that was marked as created is not"
                              " empty, {}".format(rm_file))
