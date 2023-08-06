# -*- coding:utf-8 -*-
"""
定义一些常用的装饰器
"""
import inspect
import warnings
from inspect import isfunction, isclass
from skydl.cython.common.common import PyTimerUtil


class FunctionClassDesc:
    @property
    def cls(self):
        return self._cls

    @property
    def cls_name(self):
        return self._cls_name

    @property
    def cls_module(self):
        return self._cls_module

    @property
    def is_function(self):
        return self._is_function

    @property
    def is_class(self):
        return self._is_class

    def __init__(self, cls, cls_name, cls_module, is_function, is_class):
        self._cls = cls
        self._cls_name = cls_name
        self._cls_module = cls_module
        self._is_function = is_function
        self._is_class = is_class


def is_cython(obj):
    """Check if an object is a Cython function or method"""
    # TODO(suo): We could split these into two functions, one for Cython
    # functions and another for Cython methods.
    # TODO(suo): There doesn't appear to be a Cython function 'type' we can
    # check against via isinstance. Please correct me if I'm wrong.
    def check_cython(x):
        return type(x).__name__ == "cython_function_or_method"
    # Check if function or method, respectively
    return check_cython(obj) or (hasattr(obj, "__func__") and check_cython(obj.__func__))


def is_function(function_or_class):
    return inspect.isfunction(function_or_class) or is_cython(function_or_class)


def is_class(function_or_class):
    return inspect.isclass(function_or_class)


def PrintExecTime(*args, **kwargs):
    """
    装饰器：print execution time
    * **enable_print:** enable_print=[True|False], enable flag for print function
    * **time_unit:** time_unit=["seconds"|"milliseconds"|"microseconds"|"nanoseconds"|"picoseconds"],
    the default time_unit value is "microseconds"
    usage:
    @staticmethod
    @PrintExecTime
    def add(x, y=10):
        return x + y
    @PrintExecTime(enable_print=False, time_unit="microseconds")
    def reduce(x, y=10):
        return x + y
    if __name__ == '__main__':
    add(1, 2) -> "func: add(), token time: 0.000002 microseconds!"
    :return:
    """
    # if len(args) > 0 and (inspect.isfunction(args[0]) or is_cython(args[0]) or inspect.isclass(args[0])):
    #     function_or_class = args[0]
    # else:
    #     print("Please check if using the annotaion PrintExecTime together with other multiple annotations!")
    #     def get_function_or_class(function_or_class):
    #         func_class_desc = FunctionClassDesc(function_or_class,
    #                                  function_or_class.__name__,
    #                                  function_or_class.__module__,
    #                                  is_function=is_function(function_or_class),
    #                                  is_class=is_class(function_or_class))
    #         return function_or_class
    #     function_or_class = get_function_or_class
    def make_decorator(enable_print, time_unit):
        def decorator(function_or_class):
            def decorator_func(*args, **kwargs):
                py_timer_util = PyTimerUtil(function_or_class.__name__ + "()", enable_print=enable_print, time_unit=time_unit)
                py_timer_util.start_timer()
                rv = function_or_class(*args, **kwargs)
                token_time = py_timer_util.stop_timer()
                # print(f'PrintExecTime->func: ' + function_or_class.__name__ + '()' + ', token time: {:.3f} {}!'.format(token_time, time_unit))
                return rv
            return decorator_func
        return decorator

    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # This is the case where the decorator is just @PrintExecTime
        return make_decorator(True, "microseconds")(args[0])
    else:
        error_string = ("The @PrintExecTime decorator must be applied either "
                        "with no arguments and no parentheses, for example "
                        "'@PrintExecTime', or it must be applied using some of "
                        "the arguments 'enable_print', 'time_unit',  like "
                        "'@PrintExecTime(enable_print=False, "
                        "time_unit=\"microseconds\")'.")
        assert len(args) == 0 and len(kwargs) > 0, error_string
        for key in kwargs:
            assert key in [
                "enable_print",
                "time_unit"
            ], error_string
    enable_print = kwargs["enable_print"] if "enable_print" in kwargs else True
    time_unit = kwargs["time_unit"] if "time_unit" in kwargs else "microseconds"
    return make_decorator(enable_print, time_unit)


def Override(cls):
    """Annotation for documenting method overrides.
    ```
    usage:
    class A(object):
        def __init__(self):
            pass
        def _init(self):
            pass

    class B(A):
        @PrintExecTime
        @PublicAPI
        @Override(A)
        def _init(self):
            pass
    >> B()._init()
    ```
    Arguments:
        cls (type): The superclass that provides the overriden method. If this
            cls does not actually have the method, an error is raised.
    """
    def check_override(method):
        if method.__name__ not in dir(cls):
            raise NameError("{} does not override any method of {}".format(method, cls))
        return method
    return check_override


def PublicAPI(obj):
    """Annotation for documenting public APIs.
    Public APIs are classes and methods exposed to end users of RLlib. You
    can expect these APIs to remain stable across RLlib releases.

    Subclasses that inherit from a ``@PublicAPI`` base class can be
    assumed part of the RLlib public API as well (e.g., all trainer classes
    are in public API because Trainer is ``@PublicAPI``).

    In addition, you can assume all trainer configurations are part of their
    public API as well.
    """
    return obj


def DeveloperAPI(obj):
    """Annotation for documenting developer APIs.
    Developer APIs are classes and methods explicitly exposed to developers
    for the purposes of building custom algorithms or advanced training
    strategies on top of RLlib internals. You can generally expect these APIs
    to be stable sans minor changes (but less stable than public APIs).

    Subclasses that inherit from a ``@DeveloperAPI`` base class can be
    assumed part of the RLlib developer API as well (e.g., all policy
    optimizers are developer API because PolicyOptimizer is ``@DeveloperAPI``).
    """
    return obj


def Deprecated(func):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used.
    note: it must be on subclass, should not be on superclass
    """
    def newFunc(*args, **kwargs):
        if isfunction(func):
            func_type = "function"
        elif isclass(func):
            func_type = "class"
        else:
            func_type = "type"
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn(f"Call to deprecated {func_type}: {func.__name__}.", category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    newFunc.__name__ = func.__name__
    newFunc.__doc__ = func.__doc__
    newFunc.__dict__.update(func.__dict__)
    return newFunc


def Singleton(cls):
    """
    create singleton instance
    note: it must be on subclass, should not be on superclass
    """
    def _singleton(*args, **kargs):
        if not hasattr(cls, 'instance'):
            cls.instance = cls(*args, **kargs)
        return cls.instance
    return _singleton


if __name__ == '__main__':
    @PrintExecTime(enable_print=True)
    def foo(abc, de):
        print("call foo..." + str(abc + de))

    class A(object):
        def __init__(self):
            pass

        @PublicAPI
        def _init(self):
            pass

    @Singleton
    class B(A):
        def __init__(self):
            print("call B...")
        @PrintExecTime(enable_print=True, time_unit="nanoseconds")
        @PublicAPI
        @Override(A)
        def _init(self):
            pass

    foo(11, 22)
    B()._init()
    B()._init()

    @Deprecated
    class SomeClass:
        @Deprecated
        def some_old_method(self, x, y):
            return x + y

    print(SomeClass().some_old_method(33, 44))


