def test_single_ending():
    from fil_io.select import check_file_name_ending

    assert check_file_name_ending("abc.json", "json")
    assert check_file_name_ending("abc.json", ".json")
    assert not check_file_name_ending("abc.json", "csv")
    assert not check_file_name_ending("abc.json", ".csv")


def test_multiple_endings():
    from fil_io.select import check_file_name_ending

    assert check_file_name_ending("abc.json", ("json", "csv"))
    assert check_file_name_ending("abc.json", [".json", "csv"])
    assert check_file_name_ending("abc.json", {".json", ".csv"})
    assert not check_file_name_ending("abc.json", {"csv", "xml"})
    assert not check_file_name_ending("abc.json", (".csv", "xml"))
    assert not check_file_name_ending("abc.json", [".csv", ".xml"])
