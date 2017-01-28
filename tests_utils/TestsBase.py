import unittest
from conftest import pytest_assertrepr_compare


class TestBase(unittest.TestCase):
    """
    Testing base class
    """
    def areListsEqual(self, list1, list2, equality_method=lambda x, y: x == y):
        if len(list1) != len(list2):
            raise AssertionError(
                "length of {} is not equal to length of {}\n {} != {}".format(list1, list2, len(list1), len(list2)))
        try:
            for i in range(len(list1)):
                self.areEqual(list1[i], list2[i], equality_method)
        except AssertionError as err:
            raise AssertionError("Assertion error on element {}: {}".format(i, err))

    def areEqual(self, obj1, obj2, equality_method=lambda x, y: x == y):
        if not equality_method(obj1, obj2):
            message = pytest_assertrepr_compare("==", obj1, obj2)
            if message is not None:
                raise AssertionError('\n'.join(message))
            else:
                raise AssertionError("{} != {} ".format(obj1, obj2))
