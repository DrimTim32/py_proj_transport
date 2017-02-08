"""
This file provides base class for tests, API is compatibile with unittest.TestCase
"""
import unittest

from conftest import pytest_assertrepr_compare


class TestBase(unittest.TestCase):
    """
    Testing base class
    """

    def are_lists_equal(self, list1, list2, equality_method=lambda x, y: x == y):
        """
        Checks if two lists are equal using equality method
        :param list1: first list
        :param list2: second list
        :param equality_method: equality method
        :return: None
        """
        i = 0
        if len(list1) != len(list2):
            raise AssertionError(
                "length of {} is not equal to length of {}\n {} != {}".format(list1, list2, len(list1), len(list2)))
        try:
            for i in range(len(list1)):
                self.are_equal(list1[i], list2[i], equality_method)
        except AssertionError as err:
            raise AssertionError("Assertion error on element {}: {}".format(i, err))

    def are_equal(self, obj1, obj2, equality_method=lambda x, y: x == y): # pylint: disable=R0201
        """
        Checks if two objecs are are equal using equality method
        :param obj1: first object
        :param obj2: second object
        :param equality_method: equality method
        :return: None
        """
        if not equality_method(obj1, obj2):
            message = pytest_assertrepr_compare("==", obj1, obj2)
            if message is not None:
                raise AssertionError('\n'.join(message))
            else:
                raise AssertionError("{} != {} ".format(obj1, obj2))
