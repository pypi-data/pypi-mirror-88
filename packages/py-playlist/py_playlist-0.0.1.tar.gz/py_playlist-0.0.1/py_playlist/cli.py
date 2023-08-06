import click
import click_aliases
import logging
import os


import utils
import logs
import config
import playlist


@logs.log_function
def validate_dir_list(path_list):
    validated = []
    for path in path_list:
        expanded = utils.expand_path(path)
        if os.path.isdir(expanded):
            validated.append(expanded)
        else:
            logs.logging.error(f'dir {path} is not valid')
    return validated


@click.group(invoke_without_command=True, cls=click_aliases.ClickAliasedGroup)
@click.option('--config_path', '--config', '-c', default=None, help='''set a configuration directory to be considered''')
@click.option('--playlist_path', '--playlist', '-l', default=None, help='''set the playplist dir for one run''')
@click.option('--editor', '-e', default=None, help='''set the editor for one run''')
@click.option('--music_path', '--music', '-m', 'music_path_list', multiple=True, default=None, help='''set the
        music dir for one run

        This option can be called multiple times and it will erase previous
        music paths''')
@click.option('--add_music_path', '--add_music', '-a', 'music_path_add', multiple=True, default=None, help='''adds the
        music dir for one run

        This option can be called multiple times and it will not erase previous
        music paths''')
@click.option('--player', '-p', default=None, help='''set the player for one run''')
@click.option('--save_config/', '--save/', '-s/-S', help='''updates the config with the parameters provided in this call''')
@click.option('--force_default/', '--default/', '-d/-D', help='''loads the
        default configuration''')
@click.option('--debug', 'log_level', flag_value=logging.DEBUG, help='''set the log level to debug''')
@click.option('--info', 'log_level', flag_value=logging.INFO, help='''set the log level to info''')
@click.option('--warning', 'log_level', flag_value=logging.WARNING, help='''set the log level to warning''')
@click.option('--error', 'log_level', flag_value=logging.ERROR, help='''set the log level to error''')
@click.version_option(utils.__version__)
def main(config_path, playlist_path, editor, player, save_config,
        force_default, log_level=logging.CRITICAL, music_path_list=[],
        music_path_add=[]):
    '''
    Entry point to py_playlist

    This can be called without a command to execute configurations, and can
    receive some parameters to change the behavior, calling different players
    and file editors.
    '''
    logs.start_logs(log_level)

    cleaned_music_path = validate_dir_list(music_path_list)
    cleaned_path_add = validate_dir_list(music_path_add)

    if len(music_path_list) > 0 and len(cleaned_music_path) == 0 and len(cleaned_path_add) == 0:
        logs.logging.critical(f'no music dir is valid')

    config.config_init(config_path, playlist_path, cleaned_music_path, music_path_add, editor,
        player, save_config, force_default)


@main.command(aliases=['ed', 'e'])
@click.argument('playlist_name')
def edit(playlist_name):
    '''
    open a file editor to create and edit a playlist
    '''
    playlist.edit(playlist_name)


@main.command(aliases=['pl', 'p'])
@click.argument('playlist_name')
@click.option('--shuffle', '-s', flag_value=True, help='''allows shuffling the songs''')
def play(playlist_name, shuffle=False):
    '''
    runs the playlist in the configured player
    '''
    playlist.play(playlist_name, shuffle)


@main.command(aliases=['ls', 'l'])
def list():
    '''
    show the playlists list
    '''
    playlist.list_()


@main.command(aliases=['ec', 'c'])
@click.option('--config_path', '--config', '-c', default=None, help='''set a configuration directory to be considered''')
def edit_conf(config_path):
    '''
    open a file editor to create and edit the configuration
    '''
    config.edit_config(config_path)


@main.command(aliases=['sc', 's'])
@click.option('--config_path', '--config', '-c', default=None, help='''set a configuration directory to be considered''')
def show(config_path):
    '''
    show the configuration
    '''
    config.show_config(config_path)


if __name__ == '__main__':
    main(obj={})
