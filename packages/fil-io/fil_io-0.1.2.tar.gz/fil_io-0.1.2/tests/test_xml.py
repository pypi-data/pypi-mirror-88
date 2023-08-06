from pytest import raises
from .fixtures import cwd_in_tests_root, os_path
from collections import OrderedDict

test_write_data = {"main_key": {"first_row": "value1", "second_row": 2, "third_row": ["abc", "def", 3]}}


def test_load_single(cwd_in_tests_root):
    from fil_io.xml import load_single

    loaded = load_single("./test_files/standard.xml")
    assert loaded == {
        'main_key': OrderedDict([
            ('first_row', 'value1'),
            ('second_row', '2'),
            ('third_row', ['3', 'abc', 'def'])
        ])
    }

    with raises(IsADirectoryError):
        load_single("./test_files")


def test_load_all(cwd_in_tests_root):
    from fil_io.xml import load_all

    with raises(NotADirectoryError):
        load_all("./test_files/standard.xml")

    loaded = load_all("./test_files")
    assert loaded == os_path({
        'test_files/other_file.xml': {
            'main_key': OrderedDict([
                ('first_row',
                 'value1'),
                ('second_row', '2'),
                ('_3rd_row',
                 ['3',
                  'abc',
                  'def'])
            ])
        },
        'test_files/standard.xml': {
            'main_key': OrderedDict([
                ('first_row', 'value1'),
                ('second_row', '2'),
                ('third_row',
                 ['3',
                  'abc',
                  'def'])
            ])
        }
    })


def test_load(cwd_in_tests_root):
    from fil_io.xml import load

    loaded = load("./test_files/standard.xml")
    assert loaded == {
        'main_key': OrderedDict([
            ('first_row', 'value1'),
            ('second_row', '2'),
            ('third_row', ['3', 'abc', 'def'])
        ])
    }

    loaded = load("./test_files")
    assert loaded == os_path({
        'test_files/other_file.xml': {
            'main_key': OrderedDict([
                ('first_row',
                 'value1'),
                ('second_row', '2'),
                ('_3rd_row',
                 ['3',
                  'abc',
                  'def'])
            ])
        },
        'test_files/standard.xml': {
            'main_key': OrderedDict([
                ('first_row', 'value1'),
                ('second_row', '2'),
                ('third_row',
                 ['3',
                  'abc',
                  'def'])
            ])
        }
    })


def test_write(tmp_path):
    import xmltodict
    from fil_io.xml import write

    file = str(tmp_path / "data.xml")
    write(test_write_data, file)

    loaded = dict(xmltodict.parse(open(file, "r").read()))
    assert loaded == {
        'main_key': OrderedDict([('first_row', 'value1'),
                                 ('second_row', '2'),
                                 ('third_row', ['abc', 'def', '3'])])
    }

    write(test_write_data["main_key"], file, "some_main_key")

    loaded = dict(xmltodict.parse(open(file, "r").read()))
    assert loaded == {
        'some_main_key': OrderedDict([('first_row', 'value1'),
                                 ('second_row', '2'),
                                 ('third_row', ['abc', 'def', '3'])])
    }


def test_write_not_allowed_keys(tmp_path):
    from fil_io.xml import write
    file = str(tmp_path / "data.xml")

    false_keys = [".s", "_&d%", "3fd"]

    for key in false_keys:
        test_data = {"first_row": "value1", key: 2, "third_row": ["abc", "def", 3]}

        with raises(ValueError):
            write(test_data, file)

    for key in false_keys:
        test_data = {"first_row": "value1", "second_row": 2, "third_row": ("abc", {"dict": {key: "value"}}, 3)}

        with raises(ValueError):
            write(test_data, file)
