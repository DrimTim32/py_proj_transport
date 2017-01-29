import sys
from core.simulation.passenger_group import PassengersGroup

collect_ignore = ["setup.py"]
if sys.version_info[0] <= 2:
    collect_ignore.append("tests/python_3")


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, PassengersGroup) and isinstance(right, PassengersGroup) and (op == "==" or op == "!="):
        return ['Comparing PassengersGroup instances:',
                ' vals:  {}, {} and {}, {} with operator {}'.format(left.count, left.destination, right.count,
                                                                    right.destination, op)]
    if isinstance(left, PassengersGroup) and isinstance(right, list) and op == "in":
        if all(isinstance(x, PassengersGroup) for x in right):
            setDump = ["({},{})".format(x.destination, x.count) for x in right]
            return ['List of PassengersGroup ({},{}) is not in set {}:'
                        .format(left.destination,left.count, setDump)]
