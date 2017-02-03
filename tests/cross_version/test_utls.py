"""
This file contains tests for utils class
"""
import sys

import pytest

from tests_utils.helpers import get_full_class_name


@pytest.mark.parametrize(("cls", "type_name"), [
    (list, "list"),
    (dict, "dict"),
    (tuple, "tuple"),
    (abs, "abs"),
])
def test_on_buitlin(cls, type_name):
    """Checks if builtin types are recognized properly"""
    builtin = "builtins." if sys.version_info[0] >= 3 else "__builtin__."
    assert get_full_class_name(cls) == builtin + type_name
