import tempfile
import random
import os

import py_playlist.config as config
import py_playlist.cli as cli

def test_shell_injection_prevention(cli_runner):
    try:
        config.config_init(
            config_path=None,
            save_config=False,
            force_default=True,
            music_path_list=[],
            music_path_add=[],
            editor='vim; shutdown')
        assert False
    except:
        assert True

    try:
        config.config_init(
            config_path=None,
            save_config=False,
            force_default=True,
            music_path_list=[],
            music_path_add=[],
            editor='ed')
        assert True
    except:
        assert False


    try:
        config.config_init(
            config_path=None,
            save_config=False,
            force_default=True,
            music_path_list=[],
            music_path_add=[],
            player='vlc; shutdown')
        assert False
    except:
        assert True

    try:
        config.config_init(
            config_path=None,
            save_config=False,
            force_default=True,
            music_path_list=[],
            music_path_add=[],
            editor='vlc')
        assert True
    except:
        assert False

    result = cli_runner.invoke(cli.main, ['-d', '-e', 'vim; shutdown'])
    assert result.exit_code > 0

    result = cli_runner.invoke(cli.main, ['-d', '-e', 'vim'])
    assert result.exit_code == 0

    result = cli_runner.invoke(cli.main, ['-d', '-p', 'vlc; shutdown'])
    assert result.exit_code > 0

    result = cli_runner.invoke(cli.main, ['-d', '-p', 'vlc'])
    assert result.exit_code == 0


def test_file_saving():
    with tempfile.NamedTemporaryFile(mode='r') as temp_buf:
        file_path = temp_buf.name

        try:
            config.config_init(
                config_path=file_path,
                save_config=True,
                force_default=True,
                music_path_list=[],
                music_path_add=[],
                editor='vscode',
                player='vlc')
        except:
            assert False

        data = '; '.join(temp_buf)
        assert 'vlc' in data
        assert 'vscode' in data


def test_file_creation():
    file_path = '/tmp/' + str(random.getrandbits(64))

    try:
        config.config_init(
            config_path=file_path,
            save_config=True,
            force_default=False,
            music_path_list=[],
            music_path_add=[],
            editor='vscode',
            player='vlc')

        with open(config.main_conf_path(file_path), 'r') as temp_buf:
            data = '; '.join(temp_buf)
            assert 'vlc' in data
            assert 'vscode' in data

    except:
        assert False

    os.remove(config.main_conf_path(file_path))
    os.rmdir(file_path)

def test_add_music_path():
    with tempfile.TemporaryDirectory() as tmpdirname:

        config.config_init(
            config_path=None,
            save_config=True,
            force_default=True,
            music_path_list=[],
            music_path_add=[tmpdirname])

        assert tmpdirname in config._config.music_path_list


def test_set_music_path():
    with tempfile.TemporaryDirectory() as tmpdirname:

        config.config_init(
            config_path=None,
            save_config=True,
            force_default=True,
            music_path_list=[tmpdirname],
            music_path_add=[])

        assert [tmpdirname] == config._config.music_path_list


def test_arg_spliting():
    config.config_init(
        config_path=None,
        save_config=True,
        force_default=True,
        music_path_list=[],
        music_path_add=[],
        editor_args='--verbose --debug',
        player_args='--verbose --debug')

    assert config._config.editor_args == ['--verbose', '--debug']
    assert config._config.player_args == ['--verbose', '--debug']
