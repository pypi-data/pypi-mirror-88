"""
Clarisse

A light-weighted GUI framework for Python programs.

by 1MLightyears@gmail.com

on 20201208
"""
from __future__ import absolute_import

import os
import sys
from functools import wraps

from GUI import ClrsGUI

#from .analyze import AnalyzeFunc


__all__ = ["Clarisse", "version"]

version="v0.0.2"

def Clarisse(*args, **kwargs):
    def middle(func):
        if isinstance(func,type(lambda :0)):
            @wraps(func)
            def gui_func(*default_args, **default_kwargs):
                nonlocal func,args,kwargs
                w=ClrsGUI()
                w.Parse(func,default_args,default_kwargs,*args,**kwargs)
                w.main_window.show()
                w.app.exec_()
                return w.pages[0].run_thread.ret
            return gui_func
    return middle


