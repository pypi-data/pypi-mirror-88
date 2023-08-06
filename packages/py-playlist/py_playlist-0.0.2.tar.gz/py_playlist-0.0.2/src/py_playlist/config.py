import typing as tp
import os
import subprocess
import json
import pprint

from . import utils
from . import logs

_config_path = None
_config = None

class Configurations(tp.NamedTuple):
    playlist_path: str = utils.normalize_config_path(None)
    music_path_list: tp.Optional[tp.List[str]] = utils.default_music_path()
    editor: str = os.environ.get('EDITOR', 'vim')
    player: str = 'mpv'
    player_args: tp.List[str] = []
    editor_args: tp.List[str] = []
    version: str = utils.__version__


def assert_config(config):
    '''
    asserts configuration values tu avoid shell injection attacks
    '''
    if ' ' in config.editor:
        raise Exception('Space char in editor configuration, pleas use the `editor_args` to parametrize the editor')

    if ' ' in config.player:
        raise Exception('Space char in player configuration, pleas use the `player_args` to parametrize the player') 


@logs.log_function
def main_conf_path(config_path):
    if os.path.isdir(config_path):
        return os.path.join(config_path, 'main_conf.json')
    return config_path


@logs.log_function
def default_config(config_path, **kwargs):
    '''
    default_config(config_path, **kwargs)

    Build up new configuration objetct, may receive any configuration field in
    the kwargs.

    The `config_path` must be informed to set a default `playlist_path` in the
    configuration, as it has no default value by itself.
    '''
    kwargs.setdefault('playlist_path', config_path)
    parameters = {key: value for key, value in kwargs.items() if value}
    config = Configurations(**parameters)
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
def update_config(config, music_path_list, music_path_add, **kwargs):
    obj = config._asdict()

    if music_path_list:
        obj['music_path_list'] = music_path_list
    if music_path_add:
        obj.setdefault('music_path_list', [])
        obj['music_path_list'] = tuple(( *music_path_add, *obj['music_path_list'] ))

    parameters = {key: value for key, value in kwargs.items() if value}
    obj.update(parameters)

    if isinstance(obj['player_args'], str):
        obj['player_args'] = obj['player_args'].split(' ')

    if isinstance(obj['editor_args'], str):
        obj['editor_args'] = obj['editor_args'].split(' ')

    return Configurations(**obj)

@logs.log_function
def config_init(config_path, save_config, force_default, music_path_list, music_path_add, **kwargs):

    config_path = utils.normalize_config_path(config_path)
    global _config_path
    _config_path = config_path

    logs.logging.info(f'normalized config path is {config_path}')

    main_conf_file = main_conf_path(config_path)

    logs.logging.info(f'main config file is {main_conf_file}')

    if force_default:
        logs.logging.debug(f'forced default configurations, re initializing with default values')
        config = default_config(config_path, **kwargs)
    elif not os.path.isfile(main_conf_file):
        logs.logging.debug(f'main configuration file do not exists, initializing with default values')
        config = default_config(config_path, **kwargs)
    else:
        logs.logging.debug(f'main configuration file exists, loading')
        config = load_config(config_path)
    logs.logging.info(f'loaded configuration {str(config)}')

    config = update_config(config, music_path_list, music_path_add, **kwargs)
    logs.logging.info(f'updated configuration to {str(config)}')

    if save_config:
        logs.logging.debug('saving configurations into path {config_path}')
        write_config(config, config_path)

    assert_config(config)

    global _config
    _config = config


@logs.log_function
def edit_config(config_path):
    dir_path = _config_path
    if config_path:
        dir_path = utils.normalize_config_path(config_path)
    
    path = main_conf_path(dir_path)

    if not os.path.isfile(path):
        logs.logging.critical(f'file do not exists')
        return
    
    utils.call(_config.editor, *_config.editor_args, path)


@logs.log_function
def show_config(config_path):
    config = None
    if config_path:
        dir_path = utils.normalize_config_path(config_path)
        path = main_conf_path(dir_path)
        if not os.path.isfile(path):
            logs.logging.critical(f'file do not exists')
            return
        config = load_config(path)
    else:
        config = _config
    
    pprint.pprint({**config._asdict()})
