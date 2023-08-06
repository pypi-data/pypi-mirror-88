import os
import subprocess
import random
import pprint

import config
import logs

import utils

@logs.log_function
def playlist_path(playlist_name):
    return os.path.join(config._config.playlist_path, playlist_name)


@logs.log_function
def edit(playlist_name):
    '''
    open a file editor to create and edit a playlist
    '''
    if len(config._config.music_path_list):
        os.chdir(config._config.music_path_list[0])
    subprocess.call([config._config.editor, playlist_path(playlist_name)])


@logs.log_generator
def normalized_song_gen(song_iter):
    for song_path in song_iter:
        logs.logging.debug(f'normalizing {repr(song_path)}')
        trimmed = song_path.strip()
        if not trimmed:
            logs.logging.info('empty line in playlist')
            continue
        abs_path = utils.expand_path(trimmed)
        if os.path.isfile(abs_path):
            yield abs_path
            continue

        logs.logging.info(f'song {song_path} not found as absolute path')

        for music_dir in config._config.music_path_list:
            path_in_dir = os.path.join(music_dir, trimmed)
            abs_path = utils.expand_path(path_in_dir)
            if os.path.isfile(abs_path):
                yield abs_path
            logs.logging.info(f'song {song_path} not found in {music_dir}')



@logs.log_function
def play(playlist_name, shuffle):
    '''
    runs the playlist in the configured player
    '''
    with open(playlist_path(playlist_name), 'r') as file_buffer:
        norm = list(normalized_song_gen(file_buffer))
        logs.logging.debug(f'normalized playlist is {repr(norm)}')
        if shuffle:
            logs.logging.debug(f'shuffle songs')
            random.shuffle(norm)

        subprocess.call([config._config.player, *norm])


def list_():
    pprint.pprint([*os.listdir(config._config.playlist_path)])
