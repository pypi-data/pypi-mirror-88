import pytest
from gidconfig.experimental.experimental_ini import GidAttConfigIni
import os

SAMPLE_INI_CONTENT = """[one]
string_exp = testerstr
int_exp = 6
bool_exp = yes
multiword_string = this is a test of a sentence
multiword_comma_string = this is a test of a sentence with an, comma in it

[two]
list_str_exp = -LIST- first, second, third
list_int_exp = -LIST- 1, 2, 3
list_bool_exp = -LIST- yes, no, True, false, off, on
list_mixed_exp = -LIST- big, 12, small, off, true, 69
multiword_string_list = -LIST- this is a, test of a sentence, that is split inside a list

[three]
list_bad_format = -LIST- first,second, third,     fourth

[four]
exp_datetime = -DATETIME- 2020-11-13T01:55:33
exp_timedelta = -TIMEDELTA- days: 3, hours: 1, minutes: 21, seconds: 7
exp_timedelta_neg = -TIMEDELTA- negative days: 10, hours: 6, minutes: 7, seconds: 8
"""


@pytest.fixture
def sample_ini_file(tmpdir):
    _path = tmpdir.join('sample_config.ini')
    with open(_path, 'w') as samp_conf_file:
        samp_conf_file.write(SAMPLE_INI_CONTENT)
    yield _path


@pytest.fixture
def ini_config(sample_ini_file):
    _out_cfg = GidAttConfigIni(sample_ini_file)
    _out_cfg.load()
    yield _out_cfg
