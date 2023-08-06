"""
Clrsarisse

Analyze module.
analyze the interface of a function/class.

by 1MLightyears@gmail.com

on 20201208
"""
import inspect
import types_supported
import typing

import log

__all__=["AnalyzeFunc"]

def AddAWidget(widget_type,*args, **kwargs):
    if widget_type is int:
        return types_supported.ClrsInt(*args, **kwargs)
    elif widget_type is float:
        return types_supported.ClrsFloat(*args, **kwargs)
    elif widget_type is str:
        return types_supported.ClrsString(*args, **kwargs)
    elif widget_type is bool:
        return types_supported.ClrsBool(*args,**kwargs)
    elif widget_type is list:
        return types_supported.ClrsList(*args, **kwargs)
    elif widget_type is dict:
        return types_supported.ClrsDict(*args,**kwargs)
    elif isinstance(widget_type,typing._GenericAlias):
        if widget_type._name == "List":
            return types_supported.ClrsList(ElementType=widget_type.__args__, *args, **kwargs)
        elif widget_type._name == "Dict":
            return types_supported.ClrsDict(ElementType=widget_type.__args__, *args, **kwargs)
        else:
            return types_supported.ClrsUnknown(*args, **kwargs)
    else:
        return types_supported.ClrsUnknown(*args, **kwargs)

def AnalyzeFunc(func,*args,**kwargs):
    """
    Analyze the interface of a function, depending on its args and __doc__.
    """
    arguments = inspect.getfullargspec(func)
    log.info("func={0},arguments={1}".format(func.__name__,arguments))
    widget_list=[]
    arg_names=arguments.args or []
    arg_annos = arguments.annotations or []
    arg_defaults=arguments.defaults or []
    for name in arg_names:
        if name in arg_annos:
            widget_list.append(AddAWidget(arg_annos[name], name=name, *args, **kwargs))
            widget_list[-1].adjustSize()
        else:
            widget_list.append(AddAWidget("Unknown", name=name, *args, **kwargs))
            widget_list[-1].adjustSize()
    for i in range(len(arg_defaults)):
        widget_list[-i-1].setDefault(arg_defaults[-i-1])

    # widget_list includes all the widgets needs to be displayed.
    return widget_list
