from pytest import raises, mark
from .fixtures import cwd_in_tests_root, os_path
from pathlib import Path

test_write_data = [["1", "2"], ["A", "B, C"]]
test_dict_data = {"rows": {
    "first_row": {"b": "B1", "c": "C1", "a": "A1", "d": "D1", "b_dict": {"s": "S1", "a": "A1"}},
    "second_row": {"b": "B2", "c": "C2", "a": "A2", "b_dict": {"s": "S2", "a": "A2"}}
}}


def test_load_single(cwd_in_tests_root):
    from fil_io.csv import load_single

    loaded = load_single("./test_files/pattern_1.csv")
    assert loaded == [["header1", "header2"], ["value1", "value2"]]

    with raises(IsADirectoryError):
        load_single("./test_files")


def test_load_all(cwd_in_tests_root):
    from fil_io.csv import load_all

    with raises(NotADirectoryError):
        load_all("./test_files/pattern_1.csv")

    loaded = load_all("./test_files")
    assert loaded == os_path({
        'test_files/excel_dialect.csv': [['header_a', 'header_b'],
                                           ['abc, def', 'value_b']],
        'test_files/pattern_1.csv': [['header1', 'header2'], ['value1', 'value2']],
        'test_files/pattern_2.csv': [['header_a', 'header_b'],
                                       ["'value_a", " and more'", 'value_b']],
        'test_files/quotechar_dialect.csv': [['header_a', 'header_b'],
                                               ["'abc", " def'", 'value_b']],
        'test_files/semicolon_dialect.csv': [['header_a;header_b'],
                                               ['value_a;value_b']]
    })


def test_load(cwd_in_tests_root):
    from fil_io.csv import load

    loaded = load("./test_files/pattern_1.csv")
    assert loaded == [["header1", "header2"], ["value1", "value2"]]

    loaded = load("./test_files")
    assert loaded == os_path({
        'test_files/excel_dialect.csv': [['header_a', 'header_b'],
                                           ['abc, def', 'value_b']],
        'test_files/pattern_1.csv': [['header1', 'header2'], ['value1', 'value2']],
        'test_files/pattern_2.csv': [['header_a', 'header_b'],
                                       ["'value_a", " and more'", 'value_b']],
        'test_files/quotechar_dialect.csv': [['header_a', 'header_b'],
                                               ["'abc", " def'", 'value_b']],
        'test_files/semicolon_dialect.csv': [['header_a;header_b'],
                                               ['value_a;value_b']]
    })


def test_delimiter(cwd_in_tests_root):
    from fil_io.csv import load

    loaded = load("./test_files/semicolon_dialect.csv", delimiter=";")
    assert loaded == [["header_a", "header_b"], ["value_a", "value_b"]]


def test_quotechar(cwd_in_tests_root):
    from fil_io.csv import load

    loaded = load("./test_files/quotechar_dialect.csv", quotechar="'")
    assert loaded == [['header_a', 'header_b'], ['abc, def', 'value_b']]


def test_dialect(cwd_in_tests_root):
    from fil_io.csv import load

    loaded = load("./test_files/excel_dialect.csv", dialect="excel")
    assert loaded == [['header_a', 'header_b'], ['abc, def', 'value_b']]


def test_write(tmp_path):
    import csv
    from fil_io.csv import write

    file = str(tmp_path / "data.csv")
    write(test_write_data, file)

    loaded = [i for i in csv.reader(open(file, "r"))]
    assert loaded == test_write_data


def test_write_quotechar(tmp_path):
    from fil_io.csv import write

    file = Path(tmp_path, "data.csv")
    write(test_write_data, file)

    loaded = open(file, "r").read()
    assert loaded == '"1","2"\n"A","B, C"\n'

    file = Path(tmp_path, "data.csv")
    write(test_write_data, file, quotechar="'")

    loaded = open(file, "r").read()
    assert loaded == "1,2\nA,'B, C'\n"


def test_write_delimiter(tmp_path):
    from fil_io.csv import write

    file = str(tmp_path / "data.csv")
    write(test_write_data, file, delimiter=";")

    loaded = open(file, "r").read()
    assert loaded == "1;2\nA;B, C\n"


def test_write_dialect(tmp_path):
    from fil_io.csv import write

    file = str(tmp_path / "data.csv")
    write(test_write_data, file, dialect="excel")

    loaded = open(file, "r").read()
    assert loaded == '1,2\nA,"B, C"\n'


@mark.skip("bug in datesy")
def test_write_from_dict(tmp_path):
    import csv
    from fil_io.csv import write

    file = str(tmp_path / "data.csv")
    write(test_dict_data,
          file,
          order=["a", "b", "c", "d", "b_dict"],
          main_key_name="rows",
          main_key_position=0,
          if_empty_value=None
          )

    loaded = [i for i in csv.reader(open(file, "r"))]
    assert loaded == [
        ['rows', 'a', 'b', 'c', 'd', 'b_dict'],
        ['first_row', 'A1', 'B1', 'C1', 'D1', "{'s': 'S1', 'a': 'A1'}"],
        ['second_row', 'A2', 'B2', 'C2', '', "{'s': 'S2', 'a': 'A2'}"]
    ]
