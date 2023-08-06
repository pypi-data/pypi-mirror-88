from pytest import raises
from ..fixtures import cwd_in_tests_root, os_path
from pathlib import Path


def test_all_files(cwd_in_tests_root):
    from fil_io.select import get_file_list_from_directory

    path = "./test_files_select"
    response = get_file_list_from_directory(path)
    assert os_path({
               'test_files_select/pattern_3.json',
               'test_files_select/non_fit_pattern_1.json',
               'test_files_select/pattern_2.json',
               'test_files_select/pattern_1.json',
               'test_files_select/pattern_2.csv',
               'test_files_select/pattern_1.csv'
           }) == set(response)


def test_only_json_files(cwd_in_tests_root):
    from fil_io.select import get_file_list_from_directory
    path = "./test_files_select"
    response = get_file_list_from_directory(path, file_ending=".json")
    assert os_path({
               'test_files_select/pattern_3.json',
               'test_files_select/non_fit_pattern_1.json',
               'test_files_select/pattern_2.json',
               'test_files_select/pattern_1.json',
            }) == set(response)


def test_pattern_files(cwd_in_tests_root):
    from fil_io.select import get_file_list_from_directory
    path = "./test_files_select"
    response = get_file_list_from_directory(path, pattern="pattern*")
    assert os_path({
               'test_files_select/pattern_3.json',
               'test_files_select/pattern_2.json',
               'test_files_select/pattern_1.json',
               'test_files_select/pattern_2.csv',
               'test_files_select/pattern_1.csv'
           }) == set(response)


def test_pattern_and_json_files(cwd_in_tests_root):
    from fil_io.select import get_file_list_from_directory
    path = "./test_files_select"
    response = get_file_list_from_directory(path, file_ending=".json", pattern="pattern*")
    assert os_path({
               'test_files_select/pattern_3.json',
               'test_files_select/pattern_2.json',
               'test_files_select/pattern_1.json',
           }) == set(response)


def test_single_file_as_input(cwd_in_tests_root):
    from fil_io.select import get_file_list_from_directory
    path = "./test_files_select/pattern_1.json"

    with raises(NotADirectoryError):
        get_file_list_from_directory(path)


def test_regex(cwd_in_tests_root):
    from fil_io.select import get_file_list_from_directory
    path = "./test_files_select"

    response = get_file_list_from_directory(path, regex="^pattern_[0-2].json$")
    assert os_path({
               'test_files_select/pattern_1.json',
               'test_files_select/pattern_2.json'
           }) == set(response)

    response = get_file_list_from_directory(path, file_ending="json", regex="^pattern_[0-2]$")
    assert os_path({
               'test_files_select/pattern_1.json',
               'test_files_select/pattern_2.json'
           }) == set(response)
