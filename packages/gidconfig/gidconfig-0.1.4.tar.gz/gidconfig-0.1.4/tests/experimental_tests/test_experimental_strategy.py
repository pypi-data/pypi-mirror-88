import pytest
from gidconfig.experimental.experimental_strategy import ConfigStrategos
from gidconfig.experimental.experimental_ini import GidAttConfigIni


def test_is_singleton_ini(sample_ini_file):
    _first = ConfigStrategos.borrow_config(sample_ini_file)
    _second = ConfigStrategos.borrow_config(sample_ini_file)
    assert _first is _second


def test_correct_extension(sample_ini_file):
    _cfg_ini = ConfigStrategos._create_new_config_instance(sample_ini_file)
    assert isinstance(_cfg_ini, GidAttConfigIni)
