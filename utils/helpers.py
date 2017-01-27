def fullname(o):
    return o.__module__ + "." + o.__name__


def add_property(instance, name, method):
    cls = type(instance)
    cls = type(cls.__name__, (cls,), {})
    cls.__perinstance = True
    instance.__class__ = cls
    setattr(cls, name, property(method))


def add_variable(instance, name, init_value = 0 ):
    setattr(type(instance), name, init_value)
