import logging, os, glob, re
from pathlib import Path

__doc__ = "The file_selection module provides multiple supporting functions for interaction with files"

__all__ = [
    "get_newest_file_from_directory",
    "get_file_list_from_directory",
    "return_file_list_if_directory",
    "check_file_name_ending",
]


def return_file_list_if_directory(
    path, file_ending=None, pattern=None, regex=None, return_always_list=False
):
    """
    Return all files in directory (optionally specified with options) if path is a directory

    Parameters
    ----------
    path : str
        the path to test if directory
    file_ending : str, set, optional
        the file_name ending specifying the file_name type for the files in the directory
    pattern : str, optional
        pattern for the file_names in directory to match
        ``DataFile_*.json`` where ``*`` could be a date or other strings
    regex : str, optional
        a regular_expression (`regex <https://www.tutorialspoint.com/python/python_reg_expressions.htm>`_)
        for pattern matching of the file_names
    return_always_list : bool, optional
        if a single path shall be returned as in a list

    Returns
    -------
    list, str
        if directory the list of files else the path (in a list if `return_always_list` is set)

    """
    path = Path(path)
    if path.is_dir():
        return get_file_list_from_directory(path, file_ending, pattern, regex)
    if return_always_list:
        return [path]
    raise TypeError


def check_file_name_ending(file_name, ending):
    """
    Check if the file_name has the expected file_ending

    If one of the provided endings is the file_name's ending return `True`, else `False`

    Parameters
    ----------
    file_name : str
        The file_name to check the ending for
        The file_name may contain a path, so ``file_name.ending`` as well as ``path/to/file_name.ending`` will work

    ending : str, set, list
        The desired ending or multiple desired endings
        For single entries e.g. ``.json`` or ``csv``, for multiple endings e.g. ``['.json', 'csv']``

    Returns
    -------
    bool
        `True` if the `file_name`'s ending is in the given `ending`, else `False`

    """
    # input type check
    if not isinstance(file_name, (str, Path)):
        raise TypeError(f"file_name needs to be string, {type(file_name)} provided")
    if not isinstance(ending, (str, list, set, tuple)):
        raise TypeError(
            f"ending needs to be either a list, set, tuple or a string, {type(ending)} provided"
        )

    # check if multiple endings got provided
    if not hasattr(ending, "__iter__") or isinstance(ending, str):
        ending = [ending]
    elif isinstance(ending, (tuple, set)):
        ending = list(ending)

    # remove '.' from ending if provided as first character
    for element in ending:
        if not element.startswith("."):
            ending[ending.index(element)] = "." + element

    if Path(file_name).suffix in ending:
        return True

    return False


def get_file_list_from_directory(directory, file_ending=None, pattern=None, regex=None):
    """
    Return all files (optionally filtered) from directory in a list

    Parameters
    ----------
    directory : str
        the directory containing the desired files
    file_ending : str, set, optional
        the file_name's ending specifying the file type
    pattern : str, optional
        pattern for the file_names to match
        ``DataFile_*.json`` where ``*`` could be a date or other strings
    regex : str, optional
        a regular_expression (`regex <https://www.tutorialspoint.com/python/python_reg_expressions.htm>`_)
        for pattern matching

    Returns
    -------
    list
        a list of all relative file_name directories
    """
    # input type check
    if not isinstance(directory, (str, Path)):
        raise TypeError(
            "file_name needs to be string, {} provided".format(type(directory))
        )
    if pattern and regex:
        raise ValueError(
            "only `pattern` or `regex` may be specified"
        )
    if file_ending and not isinstance(file_ending, (str, list)):
        raise TypeError(
            "ending needs to be either a list or a string, {} provided".format(
                type(file_ending)
            )
        )
    if pattern and not isinstance(pattern, str):
        raise TypeError("pattern needs to be string, {} provided".format(type(pattern)))
    if regex and not isinstance(regex, str):
        raise TypeError("regex needs to be string, {} provided".format(type(regex)))

    directory = Path(directory)
    if not directory.is_dir():
        raise NotADirectoryError(f"{directory} is not a file_directory")

    directory_str = directory.__str__() + "/"

    # get list of files from directory
    if pattern:
        if "." not in pattern:  # if no file_name ending was specified in `pattern`
            files = glob.glob(directory_str + pattern + ".*")
        else:
            files = glob.glob(directory_str + pattern)
    else:
        files = glob.glob(directory_str + "*.*")

    # delete file_names not fitting the regex
    if regex:
        if file_ending and file_ending not in regex:
            if "." != file_ending[0]:
                file_ending = "." + file_ending

            if "$" == regex[-1]:
                regex = regex[:-1] + file_ending + "$"
            else:
                regex += file_ending + "$"

        logging.debug("regex for desired files: {}".format(regex))
        for file in files.copy():
            if not bool(re.search(regex, Path(file).parts[-1])):
                files.remove(file)

    # delete file_names not of specified file_ending
    if file_ending:
        logging.debug("file_endings for desired files: {}".format(file_ending))
        for file in files.copy():
            if not check_file_name_ending(file, file_ending):
                files.remove(file)

    logging.info("{} files in directory {}: {}".format(len(files), directory, files))
    return files


def get_newest_file_from_directory(
    directory, file_ending=None, pattern=None, regex=None
):
    """
    Return the latest file_name (optionally filtered) from a directory

    Parameters
    ----------
    directory : str
        the directory where to get the latest file_name from
    file_ending : str, set, optional
        the file_name ending specifying the file_name type
    pattern : str, optional
        pattern for the file_name to match
        ``DataFile_*.json`` where ``*`` could be a date or other strings
    regex : str, optional
       a regular_expression (`regex <https://www.tutorialspoint.com/python/python_reg_expressions.htm>`_)
       for pattern matching

    Returns
    -------
    str
        the `file_name` with the latest change date

    """

    files = get_file_list_from_directory(directory, file_ending, pattern, regex)
    if not files:
        raise ValueError(f"no files in directory found")
    latest_file = max(files, key=os.path.getctime)

    return latest_file
