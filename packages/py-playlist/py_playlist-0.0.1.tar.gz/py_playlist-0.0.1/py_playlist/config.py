import typing as tp
import os
import subprocess
import json

import utils
import logs

import pprint

_config = None
_config_path = None

class Configurations(tp.NamedTuple):
    playlist_path: str
    music_path_list: tp.Optional[tp.List[str]]
    editor: str
    player: str
    version: str = utils.__version__


@logs.log_function
def __normalize_config_path(config_path = None):
    ''' Get user's configuration directory.'''
    if config_path is None:
        if os.name == 'nt':
            confdir = os.environ['APPDATA']

        elif 'XDG_CONFIG_HOME' in os.environ:
            confdir = os.environ['XDG_CONFIG_HOME']
        else: confdir = os.path.join(os.path.expanduser('~'), '.config')

        config_path = os.path.join(confdir, 'py-playlist')

    os.makedirs(config_path, exist_ok=True)

    return config_path

@logs.log_function
def main_conf_path(config_path):
    return os.path.join(config_path, 'main_conf.json')


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
def default_config(config_path, playlist_path, editor, player):
    config = Configurations(
            playlist_path = playlist_path or config_path,
            music_path_list = default_music_path(),
            editor = editor or os.environ.get('EDITOR', 'vim'),
            player = player or 'mpv'
        )
    return config


@logs.log_function
def load_config(config_path):
    with open(main_conf_path(config_path), 'r') as file_buf:
        obj = json.load(file_buf)
        return Configurations(**obj)


@logs.log_function
def write_config(config, config_path):
    obj = config._asdict()
    with open(main_conf_path(config_path), 'w') as file_buf:
        json.dump(obj, file_buf, indent=4, sort_keys=True)

@logs.log_function
def update_config(config, playlist_path, music_path_list, music_path_add, editor, player):
    obj = config._asdict()
    if playlist_path:
        obj['playlist_path'] = playlist_path
    if editor:
        obj['editor'] = editor
    if player:
        obj['player'] = player
    if music_path_list:
        obj['music_path_list'] = music_path_list
    if music_path_add:
        obj.setdefault('music_path_list', [])
        obj['music_path_list'] = tuple(( *music_path_add, *obj['music_path_list'] ))
    return Configurations(**obj)

@logs.log_function
def config_init(config_path, playlist_path, music_path_list, music_path_add, editor, player, save_config, force_default):
    config_path = __normalize_config_path(config_path)
    global _config_path
    _config_path = config_path

    logs.logging.info(f'normalized config path is {config_path}')

    main_conf_file = main_conf_path(config_path)

    logs.logging.info(f'main config file is {main_conf_file}')

    if force_default:
        logs.logging.debug(f'forced default configurations')
        config = default_config(config_path, playlist_path, editor, player)
    elif not os.path.isfile(main_conf_file):
        logs.logging.debug(f'main config file do not exists')
        config = default_config(config_path, playlist_path, editor, player)
    else:
        logs.logging.debug(f'main config file exists, loading')
        config = load_config(config_path)
    logs.logging.info(f'loaded config {config}')

    config = update_config(config, playlist_path, music_path_list,
            music_path_add, editor, player)
    logs.logging.info(f'updated config to {config}')

    if save_config:
        logs.logging.debug('saveing config')
        write_config(config, config_path)

    global _config
    _config = config

@logs.log_function
def edit_config(config_path):
    dir_path = _config_path
    if config_path:
        dir_path = __normalize_config_path(config_path)
    
    path = main_conf_path(dir_path)

    if not os.path.isfile(path):
        logs.logging.critical(f'file do not exists')
        return
    
    subprocess.call([_config.editor, path])


@logs.log_function
def show_config(config_path):
    config = None
    if config_path:
        dir_path = __normalize_config_path(config_path)
        path = main_conf_path(dir_path)
        if not os.path.isfile(path):
            logs.logging.critical(f'file do not exists')
            return
        config = load_config(path)
    else:
        config = _config
    
    pprint.pprint({**config._asdict()})
