#!/usr/bin/env python
# -*- coding: utf-8 -*-


def rescue_code(function):
    '''
    Rescue the code that it's cell been deleted but still running the notebook. 
    Via Robin's Blog: http://blog.rtwilson.com/how-to-rescue-lost-code-from-a-jupyteripython-notebook/
    '''
    import inspect
    get_ipython().set_next_input("".join(inspect.getsourcelines(function)[0]))
