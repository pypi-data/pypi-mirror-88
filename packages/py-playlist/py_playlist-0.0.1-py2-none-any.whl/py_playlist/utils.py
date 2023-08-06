import os


import logs


__version__ = '0.0.1'


@logs.log_function
def expand_path(path):
    user_expanded = os.path.expanduser(path)
    vars_expanded = os.path.expandvars(user_expanded)
    abs_path = os.path.abspath(vars_expanded)
    return abs_path
