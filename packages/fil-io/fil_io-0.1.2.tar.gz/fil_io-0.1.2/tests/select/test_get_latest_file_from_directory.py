from ..fixtures import cwd_in_tests_root, os_path


def test_get_newest_file(cwd_in_tests_root):
    from fil_io.select import get_newest_file_from_directory
    path = "test_files_newest"

    response = get_newest_file_from_directory(path)
    assert os_path("test_files_newest/newest.csv") == response


def test_get_newest_json(cwd_in_tests_root):
    from fil_io.select import get_newest_file_from_directory
    path = "test_files_newest"

    response = get_newest_file_from_directory(path, file_ending="json")
    assert os_path("test_files_newest/new.json") == response


def test_get_newest_pattern(cwd_in_tests_root):
    from fil_io.select import get_newest_file_from_directory
    path = "test_files_newest"

    response = get_newest_file_from_directory(path, pattern="old*")
    assert os_path("test_files_newest/old.json") == response


def test_get_newest_regex(cwd_in_tests_root):
    from fil_io.select import get_newest_file_from_directory
    path = "test_files_newest"

    response = get_newest_file_from_directory(path, regex="[a-z].json$")
    assert os_path("test_files_newest/new.json") == response
