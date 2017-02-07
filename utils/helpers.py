"""
This file contains helper methods to be used in meta actions
"""


def get_full_class_name(object_instance):
    """
    Returns full class name
    :param object_instance: object instance
    """
    return object_instance.__module__ + "." + object_instance.__name__


def add_property(instance, name, method):
    """
    Adds property to object
    :param instance: object where property is going to be attached
    :param name: property name
    :param method: property method
    :return: None
    """
    cls = type(instance)
    cls = type(cls.__name__, (cls,), {})
    cls.__perinstance = True  # pylint: disable=W0212
    instance.__class__ = cls
    setattr(cls, name, property(method))


def add_variable(instance, name, init_value=0):
    """
    Adds variable to object
    :param instance: object where property is going to be attached
    :param name: variable name
    :param init_value: variable init value
    :return: None
    """
    setattr(type(instance), name, init_value)
