import pytest
from gidconfig.standard.classes import ConfigHandler, Get

import os

SAMPLE_INI_CONTENT = """[one]
string_exp = testerstr
int_exp = 6
bool_exp = yes
multiword_string = this is a test of a sentence
multiword_comma_string = this is a test of a sentence with an, comma in it

[two]
list_str_exp = first, second, third
list_int_exp = 1, 2, 3
list_bool_exp = yes, no, True, false, off, on
list_mixed_exp = big, 12, small, off, true, 69
multiword_string_list = this is a, test of a sentence, that is split inside a list

[three]
list_bad_format = first,second, third,     fourth

"""


@pytest.fixture
def sample_ini_file(tmpdir):
    _path = tmpdir.join('sample_config.ini')
    with open(_path, 'w') as samp_conf_file:
        samp_conf_file.write(SAMPLE_INI_CONTENT)
    yield _path


@pytest.fixture
def ini_config(sample_ini_file):
    _out_cfg = ConfigHandler(sample_ini_file)
    yield _out_cfg
