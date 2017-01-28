import sys
from core.simulation.passenger_group import PassengersGroup

collect_ignore = ["setup.py"]
if sys.version_info[0] <= 2:
    collect_ignore.append("tests/python_3")

def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, PassengersGroup) and isinstance(right, PassengersGroup) and op == "==":
        return ['Comparing PassengersGroup instances:',
                ' vals:  {}, {} != {}, {}'.format(left.count, left.destination, right.count, right.destination)]
