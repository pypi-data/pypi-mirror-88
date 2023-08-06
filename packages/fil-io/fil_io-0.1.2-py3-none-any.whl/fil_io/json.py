from .select import *
from pathlib import Path
import logging

__doc__ = (
    "The json_file module takes care of all I/O interactions concerning json files"
)
__all__ = ["load", "load_single", "load_these", "load_all", "write"]


def load(path):
    """
    Load(s) json file(s) and returns the dictionary/-ies
    Specifying a file_name: one file will be loaded.
    Specifying a directory: all `*.json` files will be loaded.

    Parameters
    ----------
    path : str
        path to a file_name or directory

    Returns
    -------
    dict
        dictionary representing the json ``{file_name: {data}}``

    """
    files = return_file_list_if_directory(path, file_ending=".json", return_always_list=True)
    data = load_these(files)
    try:
        [value] = data.values()
        return value
    except ValueError:
        return data


def load_single(file_name):
    """
    Load a single json file

    Parameters
    ----------
    file_name : str
        file_name to load from

    Returns
    -------
    dict
        the loaded json as a dict ``{data}``

    """
    from json import load

    if Path(file_name).is_dir():
        raise IsADirectoryError("given path is a directory not a file")

    with open(Path(file_name), "r") as f:
        logging.info("loading file_name {}".format(file_name))
        return load(f)


def load_these(file_name_list):
    """
    Load specified json files and return the data in a dictionary with file_name as key

    Parameters
    ----------
    file_name_list : list
        list of file_names to load from

    Returns
    -------
    dict(dict)
        the dictionaries from the files as values of file_name as key
        ``{file_name: {data}}``

    """
    if not isinstance(file_name_list, list):
        raise TypeError("Expected list, got {}".format(type(file_name_list)))

    data = dict()
    for file in file_name_list:
        data[file] = load_single(file)

    return data


def load_all(directory):
    """
    Load all json files in the directory and return the data in a dictionary with file_name as key

    Parameters
    ----------
    directory : str
        the directory containing the json files

    Returns
    -------
    dict(dict)
        the dictionaries from the files as values of file_name as key
        ``{file_name: {data}}``
    """

    files = get_file_list_from_directory(directory, file_ending=".json")
    data = load_these(files)

    return data


def write(data, file_name, beautify=True, sort=False):
    """
    Save json from dict to file

    Parameters
    ----------
    file_name : str
        the file_name to save under. if no ending is provided, saved as .json
    data : dict
        the dictionary to be saved as json
    beautify : bool, optional
        if the data is represented in single row or human readable presented (default: human readable)
    sort : bool, optional
        if the keys shall be ordered (default: false)

    """
    if "." not in file_name:
        file_name += ".json"

    if not check_file_name_ending(file_name, "json"):
        logging.warning(
            f"file_name ending {'.' + file_name.split('.')[-1]} different to standard ({'.json'})"
        )

    logging.info(f"saving to file_name: {file_name}")

    from json import dump

    with open(Path(file_name), "w") as fp:
        if beautify:
            if sort:
                dump(data, fp, indent=4, sort_keys=True)
            else:
                dump(data, fp, indent=4)
        else:
            if sort:
                dump(data, fp, sort_keys=True)
            else:
                dump(data, fp)
