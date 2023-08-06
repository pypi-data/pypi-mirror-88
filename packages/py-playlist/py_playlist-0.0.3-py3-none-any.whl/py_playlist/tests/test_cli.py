import py_playlist.cli as cli

def test_main_cli_doc():
    assert len(cli.main.__doc__) > 100


def test_main_cli_empty_call(cli_runner):
    result = cli_runner.invoke(cli.main)
    print(result.output)
    assert result.exit_code == 0
    assert result.output == ''


def test_show_config(cli_runner):
    result = cli_runner.invoke(cli.main, ['-d', 'show'])
    print(result.output)
    assert result.exit_code == 0
    assert len(result.output) > 100


def test_set_music_dir(cli_runner):
    result = cli_runner.invoke(cli.main, ['-d', '-m', 'INVALID_DIR', '-m', '~', 'show'])
    print(result.output)
    assert result.exit_code == 0

    #validates it will expand the user dir and put it in the configurarion
    assert cli.validate_dir_list(['~'])[0] in result.output
    assert 'INVALID_DIR' not in result.output
