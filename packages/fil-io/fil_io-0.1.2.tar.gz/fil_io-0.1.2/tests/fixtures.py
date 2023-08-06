from pytest import fixture
from os import getcwd, chdir
from pathlib import Path


@fixture
def cwd_in_tests_root():
    cwd = Path.cwd()
    cwd_list = list(Path.cwd().parts)
    try:
        while cwd_list[-1] != "tests":
            cwd_list = cwd_list[:-1]
        chdir(Path(*cwd_list))
    except IndexError:
        chdir(Path.cwd() / "tests")
    yield
    chdir(cwd)


def os_path(path_string: (str, set, dict)) -> (str, set, dict):
    if isinstance(path_string, str):
        return Path(path_string).__str__()
    elif isinstance(path_string, set):
        return {Path(i).__str__() for i in path_string}
    elif isinstance(path_string, dict):
        for path in path_string.copy():
            data = path_string[path]
            del path_string[path]
            path_string[Path(path).__str__()] = data
        return path_string
