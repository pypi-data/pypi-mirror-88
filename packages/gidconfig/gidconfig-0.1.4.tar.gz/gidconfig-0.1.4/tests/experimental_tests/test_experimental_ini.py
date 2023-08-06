import pytest
from datetime import datetime, timedelta


def test_standard_values(ini_config):
    assert ini_config.one['string_exp'] == 'testerstr'
    assert ini_config.one['int_exp'] == 6
    assert ini_config.one['bool_exp'] is True
    assert ini_config.one['multiword_string'] == 'this is a test of a sentence'
    assert ini_config.one['multiword_comma_string'] == 'this is a test of a sentence with an, comma in it'


def test_list_values(ini_config):
    assert ini_config.two['list_str_exp'] == ["first", "second", "third"]
    assert ini_config.two['list_int_exp'] == [1, 2, 3]
    assert ini_config.two['list_bool_exp'] == [True, False, True, False, False, True]
    assert ini_config.two['list_mixed_exp'] == ["big", 12, "small", False, True, 69]
    assert ini_config.two['multiword_string_list'] == ["this is a", "test of a sentence", "that is split inside a list"]


def test_list_bad_format(ini_config):
    assert ini_config.three['list_bad_format'] == ["first", "second", "third", "fourth"]


def test_datetime_values(ini_config):
    assert ini_config.four['exp_datetime'] == datetime(year=2020, month=11, day=13, hour=1, minute=55, second=33)
    assert ini_config.four['exp_timedelta'] == timedelta(days=3, hours=1, minutes=21, seconds=7)
    assert ini_config.four['exp_timedelta_neg'] == timedelta(days=-10, hours=-6, minutes=-7, seconds=-8)


def test_add_options(ini_config, sample_ini_file):
    _string_test = {'new_string_key': 'new_string_value'}
    ini_config.set_one(**_string_test)
    assert ini_config.one['new_string_key'] == 'new_string_value'

    _bool_test = {'new_bool_test': True}
    ini_config.set_one(**_bool_test)
    assert ini_config.one['new_bool_test'] is True

    _integer_test = {'new_integer_test': 23}
    ini_config.set_one(**_integer_test)
    assert ini_config.one['new_integer_test'] == 23

    _list_test = {'new_list_value': [1, 2, 'alpha', 'Beta', True, False]}
    ini_config.set_two(**_list_test)
    assert ini_config.two['new_list_value'] == [1, 2, 'alpha', 'Beta', True, False]

    with open(sample_ini_file, 'r') as sample_file:
        _content = sample_file.read()
    for line in _content.splitlines():
        if '=' in line:
            _key, _value = line.split('=')
            _key = _key.strip()
            _value = _value.strip()
            if _key == 'new_string_key':
                assert _value == 'new_string_value'
            elif _key == 'new_list_value':
                assert _value == '-LIST- 1, 2, alpha, Beta, True, False'
            elif _key == 'new_bool_test':
                assert _value == 'True'
            elif _key == 'new_integer_test':
                assert _value == '23'


def test_new_section(ini_config, sample_ini_file):
    with pytest.raises(AttributeError):
        a = ini_config.five

    ini_config.new_section('five')
    assert ini_config.five == {}

    ini_config.new_section('six', sixer_int=5)
    assert ini_config.six == {'sixer_int': 5}

    with open(sample_ini_file, 'r') as sample_file:
        _content = sample_file.read()
    _section_list = [line.strip() for line in _content.splitlines() if '=' not in line]

    assert '[five]' in _section_list
    assert '[six]' in _section_list
