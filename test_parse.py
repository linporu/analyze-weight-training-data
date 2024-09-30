import pytest
from parse import clean


@pytest.mark.parametrize("valid_input, expected", [

("## 胸\n", "胸"),

("## 核心\n", "核心"),

("## 腿｜酸痛   \n", "腿"),

("## 核心（跳過）   \n", "核心")

])


def test_clean_position_expected(valid_input, expected):

	assert clean(valid_input) == expected