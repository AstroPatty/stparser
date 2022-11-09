from stparser import __version__, parse_types, get_type, check_type
import numpy as np
import pytest




def test_int():
    assert get_type("int") == int

def test_list():
    assert get_type(["int", "float", "str"]) == [int, float, str]

def test_external():
    assert get_type("numpy.ndarray") == np.ndarray

def test_dirty_list():
    assert parse_types([1, 2, 3, "str", "int"]) == ([1, 2, 3, str, int])

def test_dict():
    assert parse_types({1: "a", 2: "b", 3: "bool"}) == {1: 'a', 2: 'b', 3: bool}

def test_recursive_dict():
    assert parse_types({1: "a", 2: "list", 3: {1: "a", 2: "b", 3:  "bool", 4: "int"}}) == {1: "a", 2: list, 3: {1: "a", 2: "b", 3:  bool, 4: int}}

def test_single_falure():
    try:
        get_type("asdf")
    except Exception as e:
        assert type(e) == TypeError
    else:
        pytest.fail()

def test_complicated_failure():
    try:
        get_type("This is a test. With multiple sentences")
    except Exception as e:
        assert type(e) == TypeError
    else:
        pytest.fail()

def test_strlist_conversion_failure():
    try:
        check_type("list", "This is a test. With multiple sentences")
    except Exception as e:
        assert type(e) == TypeError
    else:
        pytest.fail()