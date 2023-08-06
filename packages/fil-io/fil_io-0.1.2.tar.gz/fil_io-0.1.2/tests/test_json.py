from pytest import raises
from .fixtures import cwd_in_tests_root, os_path

test_write_data = {"b": "B", "c": "C", "a": "A", "d": "D", "b_dict": {"s": "S", "a": "A"}}


def test_load_single(cwd_in_tests_root):
    from fil_io.json import load_single

    loaded = load_single("./test_files/pattern_1.json")
    assert loaded == {'key1': 'value1', 'key2': 2}

    with raises(IsADirectoryError):
        load_single("./test_files")


def test_load_all(cwd_in_tests_root):
    from fil_io.json import load_all

    with raises(NotADirectoryError):
        load_all("./test_files/pattern_1.json")

    loaded = load_all("./test_files")
    assert loaded == os_path({
        'test_files/non_fit_pattern_1.json': {'key1': 'value1', 'key2': 2},
        'test_files/pattern_1.json': {'key1': 'value1', 'key2': 2},
        'test_files/pattern_2.json': {'key1': 'value1', 'key2': 2},
        'test_files/pattern_3.json': {'key1': 'value1', 'key2': 2}
    })


def test_load(cwd_in_tests_root):
    from fil_io.json import load

    loaded = load("./test_files/pattern_1.json")
    assert loaded == {'key1': 'value1', 'key2': 2}

    loaded = load("./test_files")
    assert loaded == os_path({
        'test_files/non_fit_pattern_1.json': {'key1': 'value1', 'key2': 2},
        'test_files/pattern_1.json': {'key1': 'value1', 'key2': 2},
        'test_files/pattern_2.json': {'key1': 'value1', 'key2': 2},
        'test_files/pattern_3.json': {'key1': 'value1', 'key2': 2}
    })


def test_write(tmp_path):
    from json import load
    from fil_io.json import write

    file = str(tmp_path / "data.json")
    write(test_write_data, file)

    loaded = load(open(file, "r"))
    assert loaded == test_write_data


def test_write_sorted(tmp_path):
    from json import load
    from fil_io.json import write
    file = str(tmp_path / "data.json")
    write(test_write_data, file, sort=True)

    loaded = load(open(file, "r"))
    assert str(loaded) == "{'a': 'A', 'b': 'B', 'b_dict': {'a': 'A', 's': 'S'}, 'c': 'C', 'd': 'D'}"


def test_write_beautified(tmp_path):
    from fil_io.json import write

    file = str(tmp_path / "data.json")
    write({"a": "A", "b": "B"}, file, beautify=True)

    loaded = open(file, "r").read()
    assert loaded == '{\n    "a": "A",\n    "b": "B"\n}'
