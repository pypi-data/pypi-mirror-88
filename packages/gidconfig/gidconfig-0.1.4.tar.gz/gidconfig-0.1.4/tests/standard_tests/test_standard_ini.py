from gidconfig.standard.classes import ConfigHandler, Get
import pytest


def test_getlist(ini_config):
    assert ini_config.getlist('two', 'list_str_exp') == ["first", "second", "third"]
    assert ini_config.getlist('two', 'list_int_exp') == ["1", "2", "3"]
    assert ini_config.getlist('two', 'list_bool_exp') == ["yes", "no", "True", "false", "off", "on"]
    assert ini_config.getlist('two', 'list_mixed_exp') == ["big", "12", "small", "off", "true", "69"]
    assert ini_config.getlist('two', 'multiword_string_list') == ["this is a", "test of a sentence", "that is split inside a list"]
    assert ini_config.getlist('three', 'list_bad_format') == ["first", "second", "third", "fourth"]

    assert ini_config.getlist('two', 'list_str_exp', as_set=True) == {"first", "second", "third"}

    assert ini_config.getlist('one', 'string_exp') == ['testerstr']
