import os

import subprocess

from . import logs
from . import __version__


# __version__ = '0.0.2'


@logs.log_function
def expand_path(path):
    user_expanded = os.path.expanduser(path)
    vars_expanded = os.path.expandvars(user_expanded)
    abs_path = os.path.abspath(vars_expanded)
    return abs_path


@logs.log_generator
def dir_combinations():
    for name in ('Music', 'Musica', 'Download'):
        lower = name.lower()
        yield lower
        yield lower + 's'
        upper = name.upper()
        yield upper
        yield upper + 'S'
        if len(name) > 1:
            yield upper[0] + lower[1:]
            yield upper[0] + lower[1:] + 's'


@logs.log_function
def default_music_path():
    base = dir_combinations()
    base = (f'~/{n}/' for n in base)
    path_list = []
    for path in base:
        user_expanded = os.path.expanduser(path)
        vars_expanded = os.path.expandvars(user_expanded)
        abs_path = os.path.abspath(vars_expanded)
        if os.path.isdir(abs_path):
            logs.logging.info(f'found music dir as {abs_path}')
            path_list.append(abs_path)
        logs.logging.info(f'{abs_path} is not a music dir')
    return path_list


@logs.log_function
def default_config_path():
    ''' Get user's configuration directory.'''
    if os.name == 'nt':
        # windows system
        confdir = os.environ['APPDATA']

    elif 'XDG_CONFIG_HOME' in os.environ:
        confdir = os.environ['XDG_CONFIG_HOME']
    else:
        confdir = os.path.join(os.path.expanduser('~'), '.config')

    config_path = os.path.join(confdir, 'py-playlist')
    return config_path


@logs.log_function
def normalize_config_path(config_path = None):
    '''
    normalize and makes the configuration directory
    
    If `config_path` is not informed, the default user configuration path is
    used
    '''
    if config_path is None or config_path == '':
        config_path = default_config_path()
        os.makedirs(config_path, exist_ok=True)
    elif not os.path.isfile(config_path):
        os.makedirs(config_path, exist_ok=True)

    return config_path


@logs.log_function
def call(command, *args):
    if ' ' in command:
        logs.logging.critical(f'the comand "{command}" contains a space in it')
        raise Exception(f'unsafe call to command "{command}"')
    return subprocess.call([command, *args])
