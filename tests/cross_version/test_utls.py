import sys

import pytest

from tests_utils.helpers import get_full_class_name


@pytest.mark.parametrize(("obj", "type"), [
    (list, "list"),
    (dict, "dict"),
    (tuple, "tuple"),
    (abs, "abs"),
])
def test_on_buitlin(obj, type):
    builtin = "builtins." if sys.version_info[0] >= 3 else "__builtin__."
    assert get_full_class_name(obj) == builtin + type
